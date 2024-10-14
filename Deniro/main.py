import threading
import random
from deniro import Conversation
from deniro_scripted import Script
from playsound import playsound
import websockets
import asyncio
import requests

host = ''
port = 44444
device_host = requests.get("http://wtfismyip.com/text").text
done_event = threading.Event()
conv = Conversation()
script = Script()


def speak_thread():
    conv.generate_response()
    conv.textToSpeech()
    done_event.set()


async def handle(websocket):
    try:
        async for message in websocket:
            conv.set_prompt(message)

            thread = threading.Thread(target=speak_thread)
            thread.start()

            playsound(f"filler_audios/audio_{random.randint(1, 6)}.mp3")

            done_event.wait()
            conv.talk()
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")


async def main():
    while True:
        mode = input("Enter S for scripted or I for improv: ")

        if mode.upper() == "S":
            filename = input("Enter filename: ")
            script.set_script_file(filename)
            script.textToSpeech()
            script.speak()

        elif mode.upper() == "I":
            server = await websockets.serve(handle, host=host, port=port)
            print("Ready For Connections")
            print(f"\nServing on: \nhost={device_host}port={port}")
            await server.wait_closed()
        else:
            print("Invalid\n")


if __name__ == '__main__':
    asyncio.run(main())
