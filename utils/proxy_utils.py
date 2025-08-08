import re
import time
import socket
import statistics

def is_valid_ip(ip: str) -> bool:
    """
    Checks if an IP address is valid.
    """
    pattern = r"^\d{1,3}(?:\.\d{1,3}){3}$"
    if not re.match(pattern, ip):
        return False

    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

def test_proxy_latency(ip: str, port: int, timeout: int = 5, attempts: int = 3) -> float:
    """
    Measures average latency (ping) to proxy IP using socket connection.
    Returns average response time in ms, or -1 if failed.
    """
    latencies = []
    for _ in range(attempts):
        try:
            start = time.time()
            with socket.create_connection((ip, int(port)), timeout=timeout):
                end = time.time()
                latencies.append((end - start) * 1000)  # ms
        except:
            pass

    return round(statistics.mean(latencies), 2) if latencies else -1

def format_proxy(proxy: dict) -> str:
    """
    Converts a proxy dict into string format.
    """
    if proxy.get("username") and proxy.get("password"):
        return f"{proxy['ip']}:{proxy['port']}:{proxy['username']}:{proxy['password']}"
    return f"{proxy['ip']}:{proxy['port']}"
