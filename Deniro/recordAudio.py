import pyaudio
from pydub import AudioSegment
from pynput import keyboard  # Library to detect key presses
import threading

# Global variable to control recording
is_recording = False

def record_audio_to_mp3(filename, channels=1, rate=44100, chunk=2048):
    global is_recording
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []

    print("Press 'r' to start recording...")

    while not is_recording:  # Wait until recording starts
        pass

    print("Recording... Press 'r' again to stop.")
    
    while is_recording:
        try:
            data = stream.read(chunk, exception_on_overflow=False)  # Prevent overflow exceptions
            frames.append(data)
        except OSError as e:
            print(f"Warning: {e}. Retrying...")
    
    print("Stopping recording...")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Combine all chunks into a single AudioSegment
    audio_data = b''.join(frames)
    audio_segment = AudioSegment(
        data=audio_data,
        sample_width=p.get_sample_size(pyaudio.paInt16),
        frame_rate=rate,
        channels=channels
    )

    # Export the audio segment as MP3
    audio_segment.export(filename, format="mp3")
    print(f"Audio saved as {filename}")

def on_press(key):
    global is_recording
    try:
        if key.char == 'r':
            is_recording = not is_recording
    except AttributeError:
        pass

if __name__ == "__main__":
    mp3_filename = "output.mp3"

    # Start the listener for key presses in a separate thread
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Start recording audio
    record_audio_to_mp3(mp3_filename)
    
    # Stop the listener once the recording is finished
    listener.stop()
