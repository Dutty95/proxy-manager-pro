import asyncio
import aiohttp
import time
from aiohttp_socks import ProxyConnector
from typing import List, Dict, Optional
from utils.ip_info import get_ip_info

TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 10

async def check_http_proxy(session, proxy: Dict) -> str | None:
    proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
    try:
        async with session.get(TEST_URL, proxy=proxy_url, timeout=TIMEOUT) as response:
            if response.status == 200:
                return 'HTTP'
    except Exception as e:
        print(f"[HTTP] Proxy failed: {proxy['ip']}:{proxy['port']} -> {e}")
    return None


async def check_socks_proxy(proxy: Dict, version: str = 'socks5') -> str | None:
    if proxy.get("username") and proxy.get("password"):
        socks_url = f"{version}://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
    else:
        socks_url = f"{version}://{proxy['ip']}:{proxy['port']}"

    try:
        connector = ProxyConnector.from_url(socks_url)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(TEST_URL, timeout=TIMEOUT) as response:
                if response.status == 200:
                    return version.upper()
    except Exception as e:
        print(f"[{version.upper()}] Proxy failed: {proxy['ip']}:{proxy['port']} -> {e}")
    return None


async def test_proxy_speed(proxy: Dict, proxy_type: str) -> Optional[float]:
    """Measure proxy response time in milliseconds."""
    start_time = time.perf_counter()
    try:
        if proxy_type == "HTTP":
            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
            async with aiohttp.ClientSession() as session:
                async with session.get(TEST_URL, proxy=proxy_url, timeout=TIMEOUT) as response:
                    if response.status == 200:
                        elapsed = (time.perf_counter() - start_time) * 1000
                        return round(elapsed, 2)
        else:
            version = proxy_type.lower()
            if proxy.get("username") and proxy.get("password"):
                socks_url = f"{version}://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
            else:
                socks_url = f"{version}://{proxy['ip']}:{proxy['port']}"
            connector = ProxyConnector.from_url(socks_url)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(TEST_URL, timeout=TIMEOUT) as response:
                    if response.status == 200:
                        elapsed = (time.perf_counter() - start_time) * 1000
                        return round(elapsed, 2)
    except Exception:
        pass
    return None


async def check_single_proxy(proxy: Dict) -> Dict:
    result = {"proxy": proxy, "type": None, "speed": None}

    # HTTP check
    async with aiohttp.ClientSession() as session:
        proxy_type = await check_http_proxy(session, proxy)
        if proxy_type:
            result["type"] = proxy_type
            result["speed"] = await test_proxy_speed(proxy, proxy_type)
            
            # Get IP geolocation and abuse info
            ip_info = get_ip_info(proxy['ip'])
            proxy.update({
                "country": ip_info.get("country", "Unknown"),
                "country_code": ip_info.get("country_code", "XX"),
                "city": ip_info.get("city", "Unknown"),
                "is_abused": ip_info.get("is_abused", False),
                "abuse_score": ip_info.get("abuse_score", 0)
            })
            return result

    # SOCKS5 check
    proxy_type = await check_socks_proxy(proxy, 'socks5')
    if proxy_type:
        result["type"] = proxy_type
        result["speed"] = await test_proxy_speed(proxy, proxy_type)
        
        # Get IP geolocation and abuse info
        ip_info = get_ip_info(proxy['ip'])
        proxy.update({
            "country": ip_info.get("country", "Unknown"),
            "country_code": ip_info.get("country_code", "XX"),
            "city": ip_info.get("city", "Unknown"),
            "is_abused": ip_info.get("is_abused", False),
            "abuse_score": ip_info.get("abuse_score", 0)
        })
        return result

    # SOCKS4 check
    proxy_type = await check_socks_proxy(proxy, 'socks4')
    if proxy_type:
        result["type"] = proxy_type
        result["speed"] = await test_proxy_speed(proxy, proxy_type)
        
        # Get IP geolocation and abuse info
        ip_info = get_ip_info(proxy['ip'])
        proxy.update({
            "country": ip_info.get("country", "Unknown"),
            "country_code": ip_info.get("country_code", "XX"),
            "city": ip_info.get("city", "Unknown"),
            "is_abused": ip_info.get("is_abused", False),
            "abuse_score": ip_info.get("abuse_score", 0)
        })
        return result

    return result


async def check_all_proxies(proxies: List[Dict]) -> Dict[str, List[Dict]]:
    results = await asyncio.gather(*[check_single_proxy(proxy) for proxy in proxies])

    categorized = {
        "HTTP": [],
        "SOCKS5": [],
        "SOCKS4": [],
        "BAD": []
    }

    for result in results:
        proxy = result["proxy"]
        proxy_type = result["type"]
        if proxy_type:
            proxy["speed"] = result.get("speed")
            categorized[proxy_type].append(proxy)
        else:
            categorized["BAD"].append(proxy)

    return categorized
async def test_proxy_speed(proxy: Dict, proxy_type: str) -> float | None:
    """Test the speed (latency in ms) of a single proxy based on type."""
    url = TEST_URL
    timeout = TIMEOUT

    start_time = time.time()

    try:
        if proxy_type == "HTTP":
            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy_url, timeout=timeout) as response:
                    if response.status == 200:
                        return round((time.time() - start_time) * 1000, 2)

        elif proxy_type in ("SOCKS4", "SOCKS5"):
            version = proxy_type.lower()
            if proxy.get("username") and proxy.get("password"):
                socks_url = f"{version}://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
            else:
                socks_url = f"{version}://{proxy['ip']}:{proxy['port']}"

            connector = ProxyConnector.from_url(socks_url)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == 200:
                        return round((time.time() - start_time) * 1000, 2)

    except Exception as e:
        print(f"[SpeedTest-{proxy_type}] Proxy failed: {proxy['ip']}:{proxy['port']} -> {e}")
        return None