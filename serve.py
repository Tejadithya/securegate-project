import http.server
import socketserver
import os
from pathlib import Path

# Change to frontend directory
os.chdir(r"c:\Users\Teja Dithya\Music\securegate project\frontend")

PORT = 3000
Handler = http.server.SimpleHTTPRequestHandler

print(f"Starting web server on http://localhost:{PORT}")
print(f"Serving files from: {Path.cwd()}")
print(f"\nOpen your browser and go to:")
print(f"  Login Page: http://localhost:{PORT}/index.html")
print(f"  Dashboard: http://localhost:{PORT}/dashboard.html")
print(f"\nPress CTRL+C to stop the server")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
