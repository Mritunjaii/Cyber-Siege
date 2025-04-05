


### ✅ **For Window Mainly(Level-1)**

### ✅ **1. Run VS Code as Administrator**

> 🔒 Firewall changes require elevated privileges.

- Close VS Code if already open.
- Right-click the VS Code icon → **Run as Administrator**.

---

### ✅ **2. Open the Script**

- Open the folder containing `level-1.py` in VS Code.
- Open the terminal (`Ctrl + ` or View → Terminal).

---

### ✅ **3. (Optional) Setup Python Virtual Env**

```bash
python -m venv venv
venv\Scripts\activate
```

---

### ✅ **4. Install Required Packages**

Your script doesn't use any third-party libraries, so nothing to install from pip.

---

### ✅ **5. Run the Script**

For testing (without actually blocking IPs):

```bash
python level-1.py --threshold 3 --dry-run --whitelist 192.168.1.100
```

For actual firewall rule creation:

```bash
python level-1.py --threshold 3 --whitelist 192.168.1.100
```

---

### 🧪 **To Simulate Brute-Force Events (Optional Testing Trick)**

You can create a **mock version** of `get_failed_logins_windows()` to simulate fake IPs:

```python
def get_failed_logins_windows(window_minutes):
    return ["192.168.0.101", "192.168.0.101", "192.168.0.101", "10.0.0.55", "10.0.0.55"]
```

Then test how the script reacts with thresholds.

---

### 📁 Log Location

Your log file will be saved here:
```
C:\ProgramData\SSHGuardian\level-1.log
```

---




Here’s a complete single-file version of your **Universal SSH Brute Force Defender** extended with:

- ✅ **Slack & Email alerts**  
- ✅ **Adaptive blocking (24h cooldown)**  
- ✅ **Whitelist support (YAML)**  
- ✅ **Distributed attack detection (multi-IP + geolocation)**  
- ✅ **Cross-platform compatibility**

---

### ✅ **level-2**


### 📦 Sample `whitelist.yaml`

```yaml
trusted_ips:
  - 127.0.0.1
  - 192.168.1.100
```

---

### ✅ To Run:

- Linux/macOS:
  ```bash
  sudo python3 level-2.py
  ```
- Windows:
  Run **VS Code or CMD as Administrator**, then:
  ```bash
  python level-2.py
  ```

---

