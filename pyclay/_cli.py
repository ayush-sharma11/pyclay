import sys
import os
import time
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pyclay import _runtime, _renderer, _server

def run_script(script_path):
    _runtime.reset()
    try:
        with open(script_path, encoding="utf-8") as f:
            code = f.read()
        exec(code, {"__name__": "__main__"})
        html = _renderer.render_page()
        return html
    except Exception:
        # Format a friendly error page instead of crashing
        tb = traceback.format_exc()
        print(f"\n{'='*60}")
        print(f"  ERROR in {script_path}")
        print(f"{'='*60}")
        print(tb)
        print(f"{'='*60}\n")
        error_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>pyclay – Error</title>
<style>
  body {{ font-family: 'Inter', -apple-system, sans-serif; background: #0f0f17; color: #e4e4f0; margin: 0; padding: 2rem; }}
  .error-box {{ background: #1a1a2e; border: 1px solid #ef4444; border-radius: 10px; padding: 2rem; max-width: 800px; margin: 2rem auto; }}
  h1 {{ color: #ef4444; margin-top: 0; font-size: 1.4rem; }}
  pre {{ background: #111; padding: 1.2rem; border-radius: 8px; overflow-x: auto; font-size: 0.85rem; line-height: 1.6; color: #fca5a5; }}
  p {{ color: #888; font-size: 0.9rem; }}
</style></head>
<body>
  <div class="error-box">
    <h1>\u26a0 Build Error</h1>
    <pre>{_renderer._esc(tb)}</pre>
    <p>Fix the error and save your file - the page will auto-reload.</p>
  </div>
</body></html>"""
        return error_html

class _ReloadHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path

    def on_modified(self, event):
        if event.src_path.endswith(self.script_path.lstrip("./")):
            print(f"Change detected - reloading {self.script_path}")
            html = run_script(self.script_path)
            _server.update_html(html)  # push new HTML, bump timestamp

def main():
    if len(sys.argv) < 2:
        print("Usage: pyclay <command> [args]")
        print("")
        print("Commands:")
        print("  run <script.py>              Start dev server with hot reload")
        print("  build <script.py> [--out DIR] Export static HTML")
        sys.exit(1)

    command = sys.argv[1]

    if command == "build":
        if len(sys.argv) < 3:
            print("Usage: pyclay build <script.py> [--out DIR]")
            sys.exit(1)

        script_path = sys.argv[2]

        # Parse --out flag
        out_dir = "dist"
        if "--out" in sys.argv:
            idx = sys.argv.index("--out")
            if idx + 1 < len(sys.argv):
                out_dir = sys.argv[idx + 1]

        _runtime.reset()
        try:
            with open(script_path, encoding="utf-8") as f:
                code = f.read()
            exec(code, {"__name__": "__main__"})
            html = _renderer.render_page()
        except Exception:
            print(f"\nBuild failed for {script_path}:")
            traceback.print_exc()
            sys.exit(1)

        # Strip hot-reload JS from production build
        import re
        html = re.sub(r'<script>\s*let _pc_last.*?</script>', '', html, flags=re.DOTALL)

        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Copy assets/ directory to output directory if it exists
        if os.path.exists("assets"):
            import shutil
            out_assets_dir = os.path.join(out_dir, "assets")
            try:
                if os.path.exists(out_assets_dir):
                    shutil.rmtree(out_assets_dir)
                shutil.copytree("assets", out_assets_dir)
                print(f"  Assets: copied assets/ -> {out_assets_dir}")
            except Exception as e:
                print(f"  Warning: failed to copy assets folder: {e}")

        abs_path = os.path.abspath(out_path)
        print(f"Built successfully -> {abs_path}")
        print(f"  Size: {len(html):,} bytes")

    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: pyclay run <script.py> [--port PORT]")
            sys.exit(1)

        script_path = sys.argv[2]

        # Parse --port flag
        port = 8501
        if "--port" in sys.argv:
            idx = sys.argv.index("--port")
            if idx + 1 < len(sys.argv):
                port = int(sys.argv[idx + 1])

        # first render
        html = run_script(script_path)
        server = _server.serve(html, port=port)

        # watch for file changes
        handler = _ReloadHandler(script_path)
        observer = Observer()
        observer.schedule(handler, path=".", recursive=True)
        observer.start()

        print("Watching for changes... (Ctrl+C to stop)")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped.")
            observer.stop()
            server.shutdown()

        observer.join()

    else:
        print(f"Unknown command: {command}")
        print("Available commands: run, build")
        sys.exit(1)
