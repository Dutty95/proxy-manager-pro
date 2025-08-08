import os

def save_proxies_by_type(categorized_proxies, save_dir="data/validated"):
    """
    Saves proxies into separate files by type.
    """
    os.makedirs(save_dir, exist_ok=True)

    type_map = {
        "HTTP": "http_proxies.txt",
        "SOCKS5": "socks5_proxies.txt",
        "SOCKS4": "socks4_proxies.txt"
    }

    for proxy_type, filename in type_map.items():
        proxies = categorized_proxies.get(proxy_type, [])
        path = os.path.join(save_dir, filename)

        with open(path, 'w') as f:
            for proxy in proxies:
                if proxy["username"] and proxy["password"]:
                    proxy_str = f"{proxy['ip']}:{proxy['port']}:{proxy['username']}:{proxy['password']}"
                else:
                    proxy_str = f"{proxy['ip']}:{proxy['port']}"
                f.write(proxy_str + "\n")

    print(f"[+] Proxies saved to '{save_dir}'")
