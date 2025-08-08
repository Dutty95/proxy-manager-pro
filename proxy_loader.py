import os
import re

def load_proxies(file_path):
    """
    Loads a list of proxies from a file.
    Supports formats:
        - IP:PORT
        - IP:PORT:USERNAME:PASSWORD
    """
    proxies = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Proxy file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Match formats
        match = re.match(r'^(\d{1,3}(?:\.\d{1,3}){3}):(\d{2,5})(?::(\w+):(\S+))?$', line)
        if match:
            ip = match.group(1)
            port = match.group(2)
            username = match.group(3)
            password = match.group(4)

            proxy_entry = {
                "ip": ip,
                "port": port,
                "username": username,
                "password": password
            }
            proxies.append(proxy_entry)
        else:
            print(f"[!] Skipping invalid proxy format: {line}")

    return proxies
