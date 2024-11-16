from transcribe import Transcriber
from improv import Responder
from pynput import keyboard
import threading

transcriber = Transcriber()
responder = Responder()
listener = None


def recording_thread():
    print("\n🎙️ Recording started... Press SPACE to stop")
    transcriber.record_audio()


def summary_thread():
    print("\n📝 Summarizing...")
    responder.summarise()
    print("✅ Summarized")

    print("\nPress SPACE to start recording")


def shift_pressed():
    global listener
    listener.stop()

    print("\n🤖 Thinking and speaking...")
    responder.respond()
    responder.speak()
    print("\nPress SPACE to start recording")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()


def space_pressed():
    if not transcriber.recording:
        transcriber.recording = True

        thread = threading.Thread(target=recording_thread)
        thread.start()

    elif transcriber.recording:
        transcriber.recording = False

        print("⏹️ Recording stopped")
        print("\n💾 Saving and transcribing...")

        transcriber.save_audio()
        transcriber.transcribe()

        print("📝 Transcription:", transcriber.prompt)
        responder.set_prompt(transcriber.prompt)

        thread = threading.Thread(target=summary_thread)
        thread.start()


def on_press(key):
    if transcriber.recording:
        if key == keyboard.Key.space:
            space_pressed()
        return
    if key == keyboard.Key.space:
        space_pressed()
    elif key == keyboard.Key.shift:
        shift_pressed()


def main():
    print("Welcome To Deniro")
    print("-----------------")
    print("Press SPACE to start recording")

    global listener
    listener = keyboard.Listener(on_press=on_press)

    listener.start()
    listener.join()


if __name__ == '__main__':
    main()
