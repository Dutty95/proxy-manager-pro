import asyncio
import os
from proxy_loader import load_proxies
from proxy_checker import check_all_proxies
from utils.proxy_saver import save_proxies_by_type
from utils.proxy_utils import test_proxy_latency, format_proxy
from utils.proxy_rotator import ProxyRotator
from proxy_router import launch_app_with_proxy
from utils.logger import get_logger

logger = get_logger("main")

def display_summary(categorized):
    logger.info("\n=== Proxy Check Summary ===")
    for proxy_type, proxies in categorized.items():
        logger.info(f"{proxy_type}: {len(proxies)} proxies")

def print_with_latency(proxies, label):
    logger.info(f"\n--- {label} Proxies with Latency ---")
    for proxy in proxies:
        latency = test_proxy_latency(proxy["ip"], proxy["port"])
        logger.info(f"{format_proxy(proxy)} - {latency if latency != -1 else 'FAIL'} ms")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    proxy_file = os.path.join(base_dir, "data", "proxies.txt")
    
    try:
        logger.info(f"Loading proxies from: {proxy_file}")
        proxy_list = load_proxies(proxy_file)

        if not proxy_list:
            logger.warning("No valid proxies found in file.")
            return

        logger.info(f"Loaded {len(proxy_list)} proxies. Starting check...\n")

        categorized = asyncio.run(check_all_proxies(proxy_list))

        display_summary(categorized)
        save_proxies_by_type(categorized)

        # Optional: print top SOCKS5 proxies with latency
        if categorized["SOCKS5"]:
            print_with_latency(categorized["SOCKS5"][:5], "Top SOCKS5")

        # === Proxy Rotation Setup ===
        rotator = ProxyRotator(categorized, interval_seconds=120, max_uses=5)

        # Example: Launch Chrome through a rotating SOCKS5 proxy
        proxy = rotator.get_next_proxy("SOCKS5")
        if proxy:
            app_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Change as needed
            launch_app_with_proxy(proxy, proxy_type="SOCKS5", app_path=app_path)
        else:
            logger.warning("No working SOCKS5 proxies available for routing.")

    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    main()
