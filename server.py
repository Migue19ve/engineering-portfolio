"""Dependency-free local portfolio server: python3 server.py [--port 8765]."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from demos import assistant_query, event_scenario, validate_quote

ROOT = Path(__file__).parent / "static"
FILES = {"/": ("index.html", "text/html; charset=utf-8"), "/app.js": ("app.js", "text/javascript; charset=utf-8"),
         "/styles.css": ("styles.css", "text/css; charset=utf-8")}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # No request or input logging.

    def respond(self, status, body, kind="application/json"):
        data = json.dumps(body).encode() if kind == "application/json" else body
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        self.wfile.write(data)

    def local_request(self):
        expected = f"127.0.0.1:{self.server.server_port}"
        hosts = {expected, f"localhost:{self.server.server_port}"}
        if self.headers.get("Host") not in hosts:
            self.respond(403, {"error": "Use the local demo address."})
            return False
        origin = self.headers.get("Origin")
        if origin and origin not in {f"http://{host}" for host in hosts}:
            self.respond(403, {"error": "Only same-origin local requests are accepted."})
            return False
        return True

    def do_GET(self):
        if not self.local_request():
            return
        path = urlsplit(self.path).path
        if path not in FILES:
            self.respond(404, {"error": "Not found"})
            return
        filename, kind = FILES[path]
        self.respond(200, (ROOT / filename).read_bytes(), kind)

    def do_POST(self):
        if not self.local_request():
            return
        self.connection.settimeout(5)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 30000:
                self.respond(413, {"error": "Request must be between 1 and 30,000 bytes."})
                return
            if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                self.respond(415, {"error": "Send application/json."})
                return
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object.")
            path = urlsplit(self.path).path
            if path == "/api/events":
                result = event_scenario()
            elif path == "/api/quote":
                result = validate_quote(data.get("csv"))
            elif path == "/api/assistant":
                result = assistant_query(data.get("query"))
            else:
                self.respond(404, {"error": "Not found"})
                return
            self.respond(200, result)
        except (ValueError, UnicodeDecodeError) as exc:
            self.respond(400, {"error": str(exc)})
        except TimeoutError:
            self.respond(408, {"error": "Request timed out."})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    print(f"Portfolio demo: http://127.0.0.1:{args.port} (Ctrl+C to stop)", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
