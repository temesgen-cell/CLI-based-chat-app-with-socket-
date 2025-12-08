import argparse
import socket
import threading
import sys


class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen()
        self.server_sock.setblocking(True)
        self.clients = {}  # sock -> {'thread': t, 'addr': addr, 'username': name}
        self.lock = threading.Lock()

    def start(self):
        print(f'Listening on {(self.host, self.port)}')
        try:
            while True:
                conn, addr = self.server_sock.accept()
                print(f'Accepted connection from {addr}')
                t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                with self.lock:
                    self.clients[conn] = {'thread': t, 'addr': addr, 'username': None}
                t.start()
        except KeyboardInterrupt:
            print('\nCaught KeyboardInterrupt, shutting down')
        finally:
            self.shutdown()

    def handle_client(self, conn: socket.socket, addr):
        try:
            while True:
                try:
                    data = conn.recv(4096)
                except ConnectionResetError:
                    break
                if not data:
                    break

                text = None
                try:
                    text = data.decode('utf-8', errors='ignore')
                except Exception:
                    text = None

                if text and text.startswith('/join '):
                    username = text[len('/join '):].strip()
                    with self.lock:
                        self.clients[conn]['username'] = username
                    welcome = f'-- {username} joined from {addr} --'
                    self.broadcast(welcome.encode('utf-8'), exclude=conn)
                    continue

                # broadcast received data to others, prefixed with username if known
                sender_name = None
                with self.lock:
                    sender_name = self.clients.get(conn, {}).get('username')
                if sender_name:
                    out = f'{sender_name}: {text}' if text is not None else b''
                    payload = out.encode('utf-8') if isinstance(out, str) else out
                else:
                    payload = data

                self.broadcast(payload, exclude=conn)

        finally:
            # client disconnect
            with self.lock:
                info = self.clients.pop(conn, None)
            if info and info.get('username'):
                leave_msg = f'-- {info.get("username")} left --'
                self.broadcast(leave_msg.encode('utf-8'))
            try:
                conn.close()
            except Exception:
                pass
            print(f'Connection closed: {addr}')

    def broadcast(self, data: bytes, exclude: socket.socket = None):
        with self.lock:
            # send to a snapshot of current clients
            conns = list(self.clients.keys())
        for c in conns:
            if c is exclude:
                continue
            try:
                c.sendall(data)
            except Exception:
                # if sending fails, close and remove client
                with self.lock:
                    info = self.clients.pop(c, None)
                try:
                    c.close()
                except Exception:
                    pass

    def shutdown(self):
        print('Shutting down server and closing connections...')
        with self.lock:
            conns = list(self.clients.keys())
            self.clients.clear()
        for c in conns:
            try:
                c.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                c.close()
            except Exception:
                pass
        try:
            self.server_sock.close()
        except Exception:
            pass


def main(argv=None):
    parser = argparse.ArgumentParser(description='Simple threaded chat server')
    parser.add_argument('--host', '-H', default='0.0.0.0', help='Host to bind (default: 0.0.0.0)')
    parser.add_argument('--port', '-p', type=int, default=12345, help='Port to bind (default: 12345)')
    args = parser.parse_args(argv)

    server = ChatServer(host=args.host, port=args.port)
    server.start()


if __name__ == '__main__':
    main()