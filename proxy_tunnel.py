import socketserver
from http.server import BaseHTTPRequestHandler
import threading
import socks
import socket

_active_server = None
_active_thread = None
_active_proxy = None

class ProxyTunnelHandler(BaseHTTPRequestHandler):
    upstream_proxy = None  # Tuple: (type, ip, port, username, password)

    def do_CONNECT(self):
        self.send_error(405, "CONNECT method not allowed in this tunnel.")

    def do_GET(self):
        try:
            host_header = self.headers.get('Host')
            if not host_header:
                self.send_error(400, "No Host header.")
                return

            hostname = host_header.split(':')[0]
            port = 80  # Default for HTTP

            proxy_type, ip, proxy_port, username, password = ProxyTunnelHandler.upstream_proxy

            sock = socks.socksocket()
            sock.set_proxy(proxy_type, ip, int(proxy_port), True, username, password)
            sock.connect((hostname, port))

            # Send GET request manually
            sock.sendall(f"GET {self.path} HTTP/1.1\r\nHost: {host_header}\r\n\r\n".encode())

            response = sock.recv(8192)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response)
            sock.close()

        except Exception as e:
            self.send_error(500, f"Proxy tunnel error: {e}")

def start_proxy_tunnel(proxy, local_port=8888):
    global _active_server, _active_thread, _active_proxy

    proxy_type_map = {"SOCKS5": socks.SOCKS5, "SOCKS4": socks.SOCKS4, "HTTP": socks.HTTP}
    proxy_type = proxy_type_map.get(proxy.get("type", "SOCKS5").upper())

    new_proxy = (proxy_type, proxy["ip"], proxy["port"], proxy.get("username"), proxy.get("password"))

    # Check if proxy has changed
    if _active_proxy == new_proxy and _active_server:
        print("[✓] Tunnel already running with this proxy.")
        return

    # Shut down old server if running
    if _active_server:
        print("[~] Stopping previous tunnel...")
        _active_server.shutdown()
        _active_thread.join()

    ProxyTunnelHandler.upstream_proxy = new_proxy
    _active_proxy = new_proxy

    _active_server = socketserver.ThreadingTCPServer(("localhost", local_port), ProxyTunnelHandler)
    _active_thread = threading.Thread(target=_active_server.serve_forever)
    _active_thread.daemon = True
    _active_thread.start()

    print(f"[+] Proxy tunnel running at http://127.0.0.1:{local_port} through {proxy['ip']}:{proxy['port']}")
