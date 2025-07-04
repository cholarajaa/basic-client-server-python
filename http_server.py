import http.server
import socketserver
import json
import os
import signal
import sys

PORT = 9000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ping':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'pong'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path.startswith('/files/'):
            file_path = self.path[7:]
            if os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File Not Found')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"serving at port {PORT}")
        httpd.serve_forever()

def shutdown_server(signum, frame):
    print("shutting down server")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)

    run_server()
