import http.server
import threading
import webbrowser
import time
import os
import mimetypes

_html_content = ""
_last_modified = 0

class _Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/poll":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(_last_modified).encode())
            return

        # Serve static assets and favicon.ico safely from assets folder
        normalized_path = self.path.lstrip("/")
        is_assets = normalized_path.startswith("assets/")
        is_favicon = normalized_path == "favicon.ico"

        if is_assets or is_favicon:
            local_path = normalized_path
            if is_favicon:
                local_path = os.path.join("assets", "favicon.ico")

            abs_assets_dir = os.path.abspath("assets")
            abs_local_path = os.path.abspath(local_path)

            if os.path.exists(abs_local_path) and os.path.commonpath([abs_assets_dir, abs_local_path]) == abs_assets_dir:
                try:
                    with open(abs_local_path, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    mime_type, _ = mimetypes.guess_type(abs_local_path)
                    if mime_type:
                        self.send_header("Content-type", mime_type)
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f"Error reading file: {e}".encode())
                    return
            else:
                if is_assets:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"File not found")
                    return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(_html_content.encode("utf-8"))

    def log_message(self, format, *args):
        pass

def update_html(html):
    global _html_content, _last_modified
    _html_content = html
    _last_modified = time.time()

def serve(html, port=8501):
    global _html_content, _last_modified
    _html_content = html
    _last_modified = time.time()

    # Try the requested port, fall back to the next available in range
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            server = http.server.HTTPServer(("", port + attempt), _Handler)
            actual_port = port + attempt
            break
        except OSError:
            if attempt < max_attempts - 1:
                print(f"Port {port + attempt} in use, trying {port + attempt + 1}...")
            else:
                print(f"Could not find an available port in range {port}-{port + max_attempts - 1}")
                raise

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    print(f"Running on http://localhost:{actual_port}")
    webbrowser.open(f"http://localhost:{actual_port}")

    return server
