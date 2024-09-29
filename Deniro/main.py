import threading
import socket
import random
from deniro import Conversation
from playsound import playsound

host = ''
port = 12121
done_event = threading.Event()


def speak_thread(conv):
    conv.generate_response()
    conv.speak()
    done_event.set()


def handle(conn, addr):
    conv = Conversation()

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024).decode()
            if data:
                conv.set_prompt(data)

                thread = threading.Thread(target=speak_thread, args=(conv,))
                thread.start()

                playsound(f"filler_audios/audio_{random.randint(1, 6)}.mp3")

                done_event.wait()
                conv.talk()




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
