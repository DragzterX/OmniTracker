import os
import sys
import io
import time
import socket
import threading
import urllib.request
from pathlib import Path

# Fix for pythonw.exe where sys.stdout and sys.stderr are None
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

# Ensure root and backend directories are in sys.path
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(BACKEND_DIR))

# Change current working directory to ROOT_DIR
os.chdir(ROOT_DIR)

def find_available_port(default_port=8000):
    for port in range(default_port, default_port + 50):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return default_port

def wait_for_server(port, timeout=12):
    start = time.time()
    url = f"http://127.0.0.1:{port}/api/health"
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'OmniTrackerDesktop'})
            with urllib.request.urlopen(req, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.1)
    return False

def start_server(port):
    try:
        log_msg("Uvicorn background thread starting...")
        import uvicorn
        from app.main import app
        # Run uvicorn quietly with log_config=None so it doesn't fail on pythonw
        uvicorn.run(app, host="127.0.0.1", port=port, log_config=None, access_log=False)
        log_msg("Uvicorn server exited.")
    except Exception as exc:
        import traceback
        log_msg(f"Exception in start_server: {traceback.format_exc()}")

def log_msg(msg):
    try:
        with open(ROOT_DIR / "desktop_app.log", "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
            f.flush()
    except Exception:
        pass

def run():
    log_msg("OmniTracker desktop application starting...")
    port = find_available_port(8000)
    log_msg(f"Selected port: {port}")
    
    server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    server_thread.start()

    # Wait for FastAPI to initialize and respond
    ready = wait_for_server(port)
    log_msg(f"FastAPI readiness check result: {ready}")

    try:
        import webview
        icon_path = str(ROOT_DIR / "icon.ico") if (ROOT_DIR / "icon.ico").exists() else None

        window = webview.create_window(
            title="OmniTracker",
            url=f"http://127.0.0.1:{port}",
            width=1340,
            height=880,
            min_size=(960, 640),
            background_color="#0b0f19"
        )
        log_msg("Window created, starting GUI loop...")
        webview.start(icon=icon_path)
        log_msg("GUI loop ended by user closing window. Exiting.")
    except Exception as e:
        import traceback
        log_msg(f"Error in webview execution: {traceback.format_exc()}")
    
    sys.exit(0)

if __name__ == "__main__":
    run()
