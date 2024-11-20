from transcribe import Transcriber
from improv import Responder
from scripted import Script
from interview import Interviewer
from pynput import keyboard
import threading

transcriber = Transcriber()
responder = Responder()
script = Script()
interviewer = Interviewer()

listener = None


def recording_thread():
    print("\n🎙️ Recording started... Press 1 to stop")
    transcriber.record_audio()



def summary_thread():
    print("\n📝 Summarizing...")
    responder.summarise()
    print("✅ Summarized")

    print("\nPress 1 to start recording")

def talk():
    responder.talk()
    print("\nPress 1 to start recording")


def shift_pressed():
    global listener
    listener.stop()

    print("\n🤖 Thinking...")
    responder.respond()
    responder.speak()
    print("\nResponse Ready, Press 9 To Play")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

def q_and_a():
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
        interviewer.set_prompt(transcriber.prompt)
        interviewer.generate_response()
        interviewer.textToSpeech()
        interviewer.talk()

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
        if key == keyboard.KeyCode.from_char('1'):
            space_pressed()
        return
    if key == keyboard.KeyCode.from_char('1'):
        space_pressed()
    elif key == keyboard.KeyCode.from_char('5'):
        shift_pressed()
    elif key == keyboard.KeyCode.from_char('9'):
        talk()


def on_press_question(key):
    if key == keyboard.KeyCode.from_char('1'):
        q_and_a()


def interview_mode():
    print("Welcome To Deniro")
    print("-----------------")
    print("Press 1 to start recording")

    global listener
    listener = keyboard.Listener(on_press=on_press_question)
    listener.start()
    listener.join()


def improv_mode():
    print("Welcome To Deniro")
    print("-----------------")
    print("Press 1 to start recording")

    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()


def scripted_mode():
    filename = input("Enter filename: ")
    script.set_script_file(filename)
    script.textToSpeech()
    script.speak()


def main():
    while True:
        print("\nSelect a mode:")
        print("i - Improv Mode")
        print("s - Scripted Mode")
        print("q - Question Mode")

        choice = input("Enter your choice: ").lower()

        match choice:
            case 'i':
                improv_mode()
            case 's':
                scripted_mode()
            case 'q':
                interview_mode()
            case _:
                print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
