import threading
import socket
from deniro import Conversation


host = ''
port = 1212


def handle(conn, addr):
    conv = Conversation()

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024).decode()
            if data:
                conv.set_prompt(data)
                conv.generate_response()
                conv.speak()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle, args=(conn, addr))
            thread.start()


if __name__ == '__main__':
    main()
