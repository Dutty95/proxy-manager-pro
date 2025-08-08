import time
import random
import threading
import asyncio
from proxy_checker import test_proxy_speed 

class ProxyRotator:
    def __init__(self, categorized_proxies, interval_seconds=60, max_uses=10,
                 speed_threshold_ms=3000, use_relative_threshold=False):
        self.categorized = categorized_proxies
        self.interval = interval_seconds
        self.max_uses = max_uses
        self.speed_threshold = speed_threshold_ms
        self.use_relative = use_relative_threshold

        self.current_proxy = None
        self.usage_count = 0
        self.last_rotation_time = 0
        self.lock = threading.Lock()

        self.average_speed = self.calculate_average_speed()
        self.monitoring = False
        self.monitor_thread = None
        self.proxy_type = "SOCKS5"

    def calculate_average_speed(self):
        all_speeds = []
        for proxies in self.categorized.values():
            for proxy in proxies:
                speed = proxy.get("speed")
                if speed:
                    all_speeds.append(speed)
        return sum(all_speeds) / len(all_speeds) if all_speeds else 1000

    def needs_rotation(self, proxy_speed):
        if self.use_relative:
            return proxy_speed > (self.average_speed * 2)
        else:
            return proxy_speed > self.speed_threshold

    def get_next_proxy(self, proxy_type="SOCKS5", current_speed=None):
        with self.lock:
            now = time.time()
            self.proxy_type = proxy_type.upper()
            proxies = self.categorized.get(self.proxy_type, [])

            if not proxies:
                return None

            should_rotate = (
                self.current_proxy is None or
                self.usage_count >= self.max_uses or
                now - self.last_rotation_time >= self.interval or
                (current_speed is not None and self.needs_rotation(current_speed))
            )

            if should_rotate:
                self._rotate_proxy()

            self.usage_count += 1
            return self.current_proxy

    def _rotate_proxy(self):
        proxies = self.categorized.get(self.proxy_type, [])
        if not proxies:
            self.current_proxy = None
            return

        available = [p for p in proxies if p != self.current_proxy]
        if not available:
            available = proxies

        self.current_proxy = random.choice(available)
        self.last_rotation_time = time.time()
        self.usage_count = 0

    def start_monitoring(self, proxy_type="SOCKS5"):
        self.proxy_type = proxy_type.upper()
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False

    def _monitor_loop(self):
        while self.monitoring:
            time.sleep(10)
            try:
                with self.lock:
                    current = self.current_proxy
                    if not current:
                        continue
                    speed = asyncio.run(test_proxy_speed(current, self.proxy_type))
                    if speed is None:
                        continue
                    if self.needs_rotation(speed):
                        print(f"[ProxyRotator] Speed too high ({speed}ms). Rotating proxy...")
                        self._rotate_proxy()
            except Exception as e:
                print(f"[ProxyRotator] Monitor error: {e}")
