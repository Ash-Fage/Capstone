import threading
import socket
import random
from deniro import Conversation
from deniro_scripted import Script
from playsound import playsound

host = ''
port = 1212
done_event = threading.Event()
conv = Conversation()
script = Script()


def speak_thread(conv):
    conv.generate_response()
    conv.textToSpeech()
    done_event.set()


def handle(conn, addr):
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
    while True:
        mode = input("Enter S for scripted or I for improv: ")

        if mode.upper() == "S":
            filename = input("Enter filename: ")
            script.set_script_file(filename)
            script.textToSpeech()
            script.speak()

        elif mode.upper() == "I":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                s.listen()

                while True:
                    conn, addr = s.accept()
                    thread = threading.Thread(target=handle, args=(conn, addr))
                    thread.start()

        else:
            print("Invalid\n")


if __name__ == '__main__':
    main()
