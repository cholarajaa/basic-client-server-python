# Basic server and client architecture using http.server and socket

## http.server
There are two endpoints added to the MyHandler class
1. /ping responds {"message": "pong"}
2. /files/test.txt responds with file if files exists if not throws 404
```bash
    python http_server.py 
```

## client
to access the endpoints
```bash
    curl http://localhost:9000/ping

    curl http://localhost:9000/files/test.txt
```

### Socket server
```bash
    # To run server
    python client-server-socket.py server

    # To run client
    python client-server-socket.py
```
