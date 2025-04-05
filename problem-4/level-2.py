import os
import sys
import platform
import re
import subprocess
import json
import smtplib
import yaml
import time
import requests
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from collections import defaultdict

# === CONFIG ===
BLOCK_LOG = "ssh_defender_blocks.json"
WHITELIST_FILE = "whitelist.yaml"
THRESHOLD = 5
ALERT_EMAIL = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_TO = "admin@example.com"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/XXX/XXX"
GEO_API = "http://ip-api.com/json/"

# === GLOBALS ===
failed_attempts = defaultdict(list)   # {ip: [timestamps]}
attack_clusters = defaultdict(set)    # {username: {ip}}

# === UTILS ===

def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return []
    with open(WHITELIST_FILE) as f:
        data = yaml.safe_load(f)
        return data.get("trusted_ips", [])

def log_block(ip):
    data = load_blocks()
    now = datetime.now()
    data[ip] = {
        "blocked_at": now.isoformat(),
        "expires_at": (now + timedelta(hours=24)).isoformat()
    }
    with open(BLOCK_LOG, "w") as f:
        json.dump(data, f)

def load_blocks():
    if not os.path.exists(BLOCK_LOG):
        return {}
    with open(BLOCK_LOG, "r") as f:
        return json.load(f)

def unblock_expired():
    data = load_blocks()
    now = datetime.now()
    for ip, info in list(data.items()):
        if datetime.fromisoformat(info["expires_at"]) < now:
            unblock_ip(ip)
            del data[ip]
    with open(BLOCK_LOG, "w") as f:
        json.dump(data, f)

def notify_email(ip, user, attempts, severity, timestamp):
    html = f"""
    <html>
        <body>
            <h3 style='color:{'red' if severity == 'high' else 'orange'};'>🚨 SSH Alert</h3>
            <p><b>IP:</b> {ip}<br>
            <b>User:</b> {user}<br>
            <b>Attempts:</b> {attempts}<br>
            <b>Time:</b> {timestamp}</p>
        </body>
    </html>
    """
    msg = MIMEText(html, "html")
    msg["Subject"] = "⚠ SSH Brute Force Alert"
    msg["From"] = ALERT_EMAIL
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(ALERT_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)

def notify_slack(ip, user, attempts, timestamp):
    payload = {
        "text": f"*🚨 SSH Brute Force Alert!*\n"
                f"- IP: `{ip}`\n"
                f"- User: `{user}`\n"
                f"- Attempts: `{attempts}`\n"
                f"- Time: `{timestamp}`"
    }
    requests.post(SLACK_WEBHOOK_URL, json=payload)

def block_ip(ip):
    if platform.system() == "Windows":
        subprocess.call(f'netsh advfirewall firewall add rule name="SSH Block {ip}" dir=in action=block remoteip={ip}', shell=True)
    elif platform.system() == "Darwin":
        subprocess.call(f"echo 'block drop from {ip} to any' | sudo pfctl -a ssh_defender -f -", shell=True)
    else:
        subprocess.call(f"sudo iptables -A INPUT -s {ip} -j DROP", shell=True)
    log_block(ip)

def unblock_ip(ip):
    if platform.system() == "Windows":
        subprocess.call(f'netsh advfirewall firewall delete rule name="SSH Block {ip}"', shell=True)
    elif platform.system() == "Darwin":
        pass  # implement pf unblock if needed
    else:
        subprocess.call(f"sudo iptables -D INPUT -s {ip} -j DROP", shell=True)

def get_ip_info(ip):
    try:
        resp = requests.get(f"{GEO_API}{ip}").json()
        return {
            "country": resp.get("country"),
            "asn": resp.get("as", "N/A"),
            "org": resp.get("org", "N/A")
        }
    except:
        return {"country": "Unknown", "asn": "N/A", "org": "N/A"}

def extract_log_entries():
    logs = ""
    if platform.system() == "Linux":
        try:
            logs = subprocess.check_output("journalctl -u ssh --no-pager", shell=True).decode()
        except:
            logs = open("/var/log/auth.log", "r").read()
    elif platform.system() == "Darwin":
        logs = subprocess.check_output("log show --predicate 'process == \"sshd\"'", shell=True).decode()
    elif platform.system() == "Windows":
        logs = subprocess.check_output('wevtutil qe Security "/q:*[System[(EventID=4625)]]"', shell=True).decode()
    return logs

def parse_attempts(logs):
    pattern = r"Failed password for (invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)"
    for match in re.finditer(pattern, logs):
        _, user, ip = match.groups()
        failed_attempts[ip].append(datetime.now())
        attack_clusters[user].add(ip)
        detect_cluster(user)
        if len(failed_attempts[ip]) >= THRESHOLD:
            process_block(ip, user)

def detect_cluster(user):
    if len(attack_clusters[user]) >= 5:
        notify_slack("multiple", user, len(attack_clusters[user]), datetime.now())

def process_block(ip, user):
    whitelist = load_whitelist()
    if ip in whitelist:
        return
    block_ip(ip)
    timestamp = datetime.now().isoformat()
    notify_email(ip, user, len(failed_attempts[ip]), "high", timestamp)
    notify_slack(ip, user, len(failed_attempts[ip]), timestamp)

# === MAIN LOOP ===

def main():
    if os.geteuid() != 0 and platform.system() != "Windows":
        print("❌ Please run as root.")
        sys.exit(1)

    print("🚀 SSH Guardian is running...")

    while True:
        try:
            logs = extract_log_entries()
            unblock_expired()
            parse_attempts(logs)
            time.sleep(60)
        except KeyboardInterrupt:
            print("Exiting.")
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
