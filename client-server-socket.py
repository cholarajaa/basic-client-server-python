#SERVER
# This script implements a simple TCP server that listens for connections and handles commands from clients.
# It responds to 'ping' commands with 'pong' and sends a file when requested.
import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 65432
FILE_PATH = 'example.txt'  # Path to the file to send

# Create the file with at least 1000 lines and 10,000 words if it doesn't exist
def create_large_example_file(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            line = "This is a sample line for the example file. " * 20  # ~20 words per line
            for i in range(1000):
                f.write(f"{i+1}: {line}\n")

create_large_example_file(FILE_PATH)

def handle_client(conn, addr):
    print(f'Connected by {addr}')
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            if message == 'ping':
                conn.sendall(b'pong')
            elif message == 'file':
                try:
                    with open(FILE_PATH, 'rb') as f:
                        file_data = f.read()
                    conn.sendall(file_data)
                except Exception as e:
                    conn.sendall(f'Error: {e}'.encode())
            else:
                conn.sendall(b'Unknown command')
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

HOST = '127.0.0.1'
PORT = 65432

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode())
        response = b''
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data
        return response

# CLIENT
# Send 'ping' command
response = send_command('ping')
print('Response to ping:', response.decode(errors='ignore'))

# Send 'file' command
response = send_command('file')
try:
    # Try to decode as text, if fails, treat as binary
    print('Response to file:', response.decode())
except UnicodeDecodeError:
    print('Received file data (binary):', len(response), 'bytes')