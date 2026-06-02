#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.request
import urllib.error
import json

PORT = 8000

APP_NAME = "andrejverity"
API_TOKEN = "993870efb16288ea796dfba0d1e6a9f6"

ENDPOINTS = [
    "https://keyfigures.api.unocha.org/api/v1/key_figures",
    "https://keyfigures.api.unocha.org/api/v1/keyfigures",
    "https://keyfigures.api.unocha.org/api/v1/key-figures",
    "https://keyfigures.api.unocha.org/api/v1/KeyFigures"
]

HEADER_OPTIONS = [
    {
        "APP-NAME": APP_NAME,
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    },
    {
        "APP-NAME": APP_NAME,
        "Ocp-Apim-Subscription-Key": API_TOKEN,
        "Accept": "application/json"
    },
    {
        "APP-NAME": APP_NAME,
        "X-API-KEY": API_TOKEN,
        "Accept": "application/json"
    },
    {
        "APP-NAME": APP_NAME,
        "api-key": API_TOKEN,
        "Accept": "application/json"
    },
    {
        "APP-NAME": APP_NAME,
        "Accept": "application/json"
    }
]

def extract_rows(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("hydra:member", "value", "data", "items", "results", "member"):
            if isinstance(data.get(key), list):
                return data[key]
    return []

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api":
            attempts = []

            for endpoint in ENDPOINTS:
                for headers in HEADER_OPTIONS:
                    try:
                        req = urllib.request.Request(endpoint, headers=headers, method="GET")
                        with urllib.request.urlopen(req, timeout=20) as res:
                            raw = res.read().decode("utf-8", errors="replace")
                            status = res.getcode()

                            try:
                                parsed = json.loads(raw)
                            except json.JSONDecodeError:
                                parsed = {"raw": raw}

                            rows = extract_rows(parsed)

                            attempts.append({
                                "endpoint": endpoint,
                                "headers": list(headers.keys()),
                                "status": status,
                                "row_count": len(rows)
                            })

                            if status == 200 and len(rows) > 0:
                                payload = {
                                    "ok": True,
                                    "endpoint": endpoint,
                                    "headers_used": list(headers.keys()),
                                    "rows": rows,
                                    "attempts": attempts
                                }
                                self.send_response(200)
                                self.send_header("Content-Type", "application/json; charset=utf-8")
                                self.end_headers()
                                self.wfile.write(json.dumps(payload).encode("utf-8"))
                                return

                    except urllib.error.HTTPError as e:
                        attempts.append({
                            "endpoint": endpoint,
                            "headers": list(headers.keys()),
                            "status": e.code,
                            "error": str(e)
                        })
                    except Exception as e:
                        attempts.append({
                            "endpoint": endpoint,
                            "headers": list(headers.keys()),
                            "status": "network-error",
                            "error": str(e)
                        })

            # If nothing worked, return debug details plus fallback sample rows
            fallback_rows = [
                {"country": "Afghanistan", "year": "2021", "value": "300000000", "source": "fallback", "provider": "fallback"},
                {"country": "Yemen", "year": "2021", "value": "280000000", "source": "fallback", "provider": "fallback"},
                {"country": "Ethiopia", "year": "2021", "value": "250000000", "source": "fallback", "provider": "fallback"},
                {"country": "Sudan", "year": "2021", "value": "200000000", "source": "fallback", "provider": "fallback"},
                {"country": "Afghanistan", "year": "2022", "value": "350000000", "source": "fallback", "provider": "fallback"}
            ]
            payload = {
                "ok": False,
                "message": "No endpoint/header combination returned non-empty data.",
                "rows": fallback_rows,
                "attempts": attempts
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        # Serve normal files
        return super().do_GET()

if __name__ == "__main__":
    print(f"Server running at http://localhost:{PORT}")
    httpd = HTTPServer(("localhost", PORT), Handler)
    httpd.serve_forever()
