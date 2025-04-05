import argparse
import platform
import subprocess
import re
import sys
import os
from datetime import datetime, timedelta

# Constants
DEFAULT_THRESHOLD = 10
WHITELIST = []

def check_privileges():
    
    if os.name != 'nt' and os.geteuid() != 0:
        sys.exit("❌ Requires sudo/root privileges to block IPs.")

def parse_args():
    parser = argparse.ArgumentParser(description="SSH Guardian - Brute-force IP blocker")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD, help="Failed attempts per minute before blocking")
    parser.add_argument("--whitelist", nargs="*", default=[], help="IP addresses to never block")
    parser.add_argument("--dry-run", action="store_true",
                    help="Don't actually block, just show what would be done")

    return parser.parse_args()

def get_os():
    return platform.system().lower()

def get_failed_logins_linux():
    with open("sample.log", "r") as f:
        logs = f.read()
    return re.findall(r'Failed password.*from (\d+\.\d+\.\d+\.\d+)', logs)


def get_failed_logins_macos():
    cmd = "log show --predicate 'process == \"sshd\"' --last 1h"
    logs = subprocess.getoutput(cmd)
    return re.findall(r'Failed password.*from (\d+\.\d+\.\d+\.\d+)', logs)

def get_failed_logins_windows(window_minutes):
    return ["192.168.0.101", "192.168.0.101", "192.168.0.101", "10.0.0.55", "10.0.0.55"]


def get_failed_logins_windows():
    
    # PowerShell Event Log parsing (requires admin privileges)
    cmd = 'powershell "Get-WinEvent -FilterHashtable @{LogName=\'Security\';ID=4625} | Format-List"'
    logs = subprocess.getoutput(cmd)
    return re.findall(r'IpAddress\s*:\s*(\d+\.\d+\.\d+\.\d+)', logs)
    # return ["192.168.0.101", "192.168.0.101", "192.168.0.101", "10.0.0.55", "10.0.0.55"]


def block_ip(ip):
    if ip in WHITELIST:
        return

    os_type = get_os()
    print(f"🚨 Blocking {ip}")
    if os_type == 'linux':
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    elif os_type == 'darwin':
        subprocess.run(["pfctl", "-t", "bruteforce", "-T", "add", ip])
    elif os_type == 'windows':
        subprocess.run(["powershell", f'New-NetFirewallRule -DisplayName "Block SSH Brute IP {ip}" -Direction Inbound -RemoteAddress {ip} -Action Block'])

def analyze_and_block(logins, threshold):
    ip_counter = {}
    for ip in logins:
        if ip not in WHITELIST:
            ip_counter[ip] = ip_counter.get(ip, 0) + 1

    for ip, count in ip_counter.items():
        if count >= threshold:
            block_ip(ip)

def main():
    args = parse_args()
    global WHITELIST
    WHITELIST = args.whitelist

    check_privileges()

    os_type = get_os()
    if os_type == 'linux':
        logins = get_failed_logins_linux()
    elif os_type == 'darwin':
        logins = get_failed_logins_macos()
    elif os_type == 'windows':
        logins = get_failed_logins_windows()
    else:
        sys.exit("❌ Unsupported OS")

    analyze_and_block(logins, args.threshold)

if __name__ == "__main__":
    main()
