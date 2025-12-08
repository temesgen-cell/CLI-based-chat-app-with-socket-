
import argparse
import socket
import threading
import sys


def receiver(sock, stop_event):
    """Background thread that receives messages and prints them."""
    try:
        while not stop_event.is_set():
            try:
                data = sock.recv(4096)
            except OSError:
                break
            if not data:
                print("\nServer closed connection.")
                stop_event.set()
                break
            # print received bytes as utf-8
            try:
                print('\n' + data.decode('utf-8'), end='\n> ', flush=True)
            except Exception:
                print('\n<binary data received>\n> ', flush=True)
    except Exception as e:
        print(f"Receiver error: {e}")
        stop_event.set()


def main():
    parser = argparse.ArgumentParser(description='CLI chat client')
    parser.add_argument('--host', '-H', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', '-p', type=int, default=12345, help='Server port (default: 12345)')
    parser.add_argument('--username', '-u', default=None, help='Username to display')
    args = parser.parse_args()

    addr = (args.host, args.port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(addr)
    except Exception as e:
        print(f"Failed to connect to {addr}: {e}")
        sys.exit(1)

    stop_event = threading.Event()
    recv_thread = threading.Thread(target=receiver, args=(sock, stop_event), daemon=True)
    recv_thread.start()

    # send a join message if username provided
    if args.username:
        try:
            sock.sendall(f"/join {args.username}".encode('utf-8'))
        except Exception:
            pass

    try:
        while not stop_event.is_set():
            try:
                msg = input('> ')
            except EOFError:
                # e.g., user pressed Ctrl-D
                break
            if not msg:
                continue
            if msg.strip() == '/quit':
                break
            try:
                sock.sendall(msg.encode('utf-8'))
            except BrokenPipeError:
                print('Connection broken. Exiting.')
                break
            except Exception as e:
                print(f'Error sending message: {e}')
                break
    except KeyboardInterrupt:
        print('\nInterrupted. Exiting.')

    # cleanup
    stop_event.set()
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except Exception:
        pass
    sock.close()
    recv_thread.join(timeout=1)


if __name__ == '__main__':
    main()
