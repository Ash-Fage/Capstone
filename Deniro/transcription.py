from pvrecorder import PvRecorder
from pynput import keyboard
import whisper
import wave
import struct


class Transcription:
    def __init__(self):
        self.recorder = PvRecorder(device_index=-1, frame_length=512)
        self.model = whisper.load_model('base.en')
        self.audio = []
        self.file = "audio.wav"
        self.recording = False
        self.result = "No Audio File Detected"

    def on_press(self, key):
        if key == keyboard.Key.shift:
            if self.recording:
                self.recording = False
            else:
                self.recording = True

    def record(self):
        self.audio = [] # reset audio recording

        print("Press SHIFT to start and stop recording")

        with keyboard.Listener(on_press=self.on_press) as listener:
            while True:
                if self.recording == True:
                    break
            listener.stop()

        print("Recording...")
        self.recorder.start()

        with keyboard.Listener(on_press=self.on_press) as listener:
            while self.recording:
                frame = self.recorder.read()
                self.audio.extend(frame)

            listener.stop()

        self.recorder.stop()
        print("Recording Stopped")
        self.save()

    def save(self):
        with wave.open(self.file, 'wb') as f:
            params = (1, 2, 16000, 512, 'NONE', 'not compressed')
            f.setparams(params)
            f.writeframes(struct.pack('h' * len(self.audio), *self.audio))

    def transcribe(self):
        self.result = self.model.transcribe(self.file, fp16=False)
        return self.result['text']
