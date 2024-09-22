from deniro import Conversation
import socket

host = ''
port = 1212
conv = Conversation()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024).decode()
                if data:
                    conv.set_prompt(data)
                    conv.generate_response()
                    conv.speak()


if __name__ == '__main__':
    main()
