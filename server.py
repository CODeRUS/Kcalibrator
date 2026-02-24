#!/usr/bin/env python3
"""
Local HTTP server for Kcalibrator web.
Serves the project directory with kcalibrator_settings.py and kcalibrator_func.py.
Serves index.html from Kcalibrator-gh. Used when opening http://localhost:PORT/ in browser.

Usage: python server.py [port]
Default port: 8876
"""
import http.server
import sys
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8876
DIR = Path(__file__).resolve().parent
INDEX_HTML = DIR.parent / "Kcalibrator-gh" / "index.html"


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def translate_path(self, path):
        if path in ("/", "/index.html"):
            return str(INDEX_HTML)
        return super().translate_path(path)


def main():
    with http.server.HTTPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"Kcalibrator server: http://localhost:{PORT}/")
        print(f"  index.html — http://localhost:{PORT}/")
        print(f"  kcalibrator_settings.py — http://localhost:{PORT}/kcalibrator_settings.py")
        print(f"  kcalibrator_func.py — http://localhost:{PORT}/kcalibrator_func.py")
        print("Open http://localhost:{}/ in browser.".format(PORT))
        print("Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
