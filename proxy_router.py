import subprocess
import os

def launch_app_with_proxy(proxy, proxy_type="HTTP", app_path=None):
    """
    Launches any executable (browser or otherwise) with a proxy.
    You can pass Chrome, Edge, Opera paths manually.
    """
    if not app_path or not os.path.exists(app_path):
        print("[!] Invalid app path.")
        return

    ip = proxy['ip']
    port = proxy['port']
    username = proxy.get('username')
    password = proxy.get('password')

    if username and password:
        proxy_url = f"{proxy_type.lower()}://{username}:{password}@{ip}:{port}"
    else:
        proxy_url = f"{proxy_type.lower()}://{ip}:{port}"

    # For Chromium-based browsers
    command = [app_path, f"--proxy-server={proxy_url}"]

    try:
        subprocess.Popen(command)
        print(f"[+] Launched {os.path.basename(app_path)} with proxy {proxy_url}")
    except Exception as e:
        print(f"[!] Failed to launch app: {e}")
