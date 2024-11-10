import threading
import socket
import random
from pynput import keyboard
from deniro import Conversation
from deniro_scripted import Script
from playsound import playsound

host = ''
port = 1212
shift_pressed = False
is_responding = False

done_event = threading.Event()
conv = Conversation()
script = Script()

part = []
part_lock = threading.Lock()


def speak_thread():
    conv.generate_response()
    conv.textToSpeech()
    done_event.set()


def respond():
    # Joins all 1 minute segments together and sends them to generate a response
    global is_responding
    is_responding = True

    with part_lock:
        prompt = ' '.join(part)
        print(prompt)
        conv.set_prompt(prompt)
        done_event.clear()

        thread = threading.Thread(target=speak_thread)  # starts generate the response in another thread
        thread.start()

        # Plays a filler audio while response is being generated in other thread
        playsound(f"filler_audios/audio_{random.randint(1, 6)}.mp3")

        done_event.wait()  # Code waits here till response is generated
        conv.talk()
        part.clear()
    is_responding = False


def handle(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024).decode()
            if data:
                if not is_responding:
                    with part_lock:
                        part.append(data)


# The three functions below are used to listen for a press of the shift key
# If shift is pressed the system will generate an improv response using respond()
def on_press(key):
    global shift_pressed
    try:
        if key == keyboard.Key.shift:
            shift_pressed = True
            print("Shift pressed, responding...")
            respond()
    except AttributeError:
        pass


def on_release(key):
    global shift_pressed
    if key == keyboard.Key.shift:
        shift_pressed = False


def listen_for_shift():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def main():
    # Setup the shift key listener in a new thread
    shift_listener_thread = threading.Thread(target=listen_for_shift)
    shift_listener_thread.daemon = True
    shift_listener_thread.start()

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
                    # Accept connections and start a new thread to support multi device connection
                    conn, addr = s.accept()
                    thread = threading.Thread(target=handle, args=(conn, addr))
                    thread.start()

        else:
            print("Invalid\n")


if __name__ == '__main__':
    main()
