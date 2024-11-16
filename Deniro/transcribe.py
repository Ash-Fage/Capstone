import whisper
import wave
import struct
from pvrecorder import PvRecorder


class Transcriber:

    def __init__(self):
        self.recorder = PvRecorder(device_index=-1, frame_length=512)
        self.model = whisper.load_model('base.en')
        self.audio = []
        self.file = "record.wav"
        self.prompt = "No Audio File Detected"
        self.recording = False

    def record_audio(self):
        self.audio = []

        self.recorder.start()

        while self.recording:
            frame = self.recorder.read()
            self.audio.extend(frame)

        self.recorder.stop()

    def transcribe(self):
        result = self.model.transcribe(self.file, fp16=False)
        self.prompt = result['text']

    def save_audio(self):
        with wave.open(self.file, 'wb') as f:
            params = (1, 2, 16000, 512, 'NONE', 'not compressed')
            f.setparams(params)
            f.writeframes(struct.pack('h' * len(self.audio), *self.audio))
