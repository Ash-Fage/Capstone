import os
import whisper
import wave
import struct
from openai import OpenAI
from pvrecorder import PvRecorder
from pynput import keyboard

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class Transcription:
    def __init__(self):
        self.recorder = PvRecorder(device_index=-1, frame_length=512)
        self.model = whisper.load_model('base.en')
        self.audio = []
        self.file = "audio.wav"
        self.recording = False
        self.prompt = "No Audio File Detected"
        self.response = "Please record a prompt"

        self.messages = [{
            "role": "system",
            "content": 'You are a robot named Robot DeNiro in an improv comedy show about AI.'
                       'You are sarcastic funny and self deprecating with dark humour. You always '
                       'limit your response to 3 to 5 sentences'
                       'You output one of the following EMOTIONS = HAPPY, SAD, ANGRY, NEUTRAL, '
                       'SURPRISED, DISGUSTED, FEARFUL, SARCASTIC, CHEEKY attached with the '
                       'sentiment of each sentence'
                       'An emotion should be output in the format [EMOTION]. Each and every '
                       'sentence you output should should have an emotion attached to it'
                       'You do not ever say the words "but hey"'
        }]

    def on_press(self, key):
        if key == keyboard.Key.shift:
            if self.recording:
                self.recording = False
            else:
                self.recording = True

    def record(self):
        self.audio = []  # reset audio recording

        print("Press SHIFT to start and stop recording")

        with keyboard.Listener(on_press=self.on_press) as listener:
            while True:
                if self.recording:
                    print("Recording...")
                    self.recorder.start()

                    while self.recording:
                        frame = self.recorder.read()
                        self.audio.extend(frame)

                    break

                if self.audio:
                    self.recorder.stop()
                    break

            listener.stop()

        print("Recording Stopped\n")
        self.save()

    def save(self):
        with wave.open(self.file, 'wb') as f:
            params = (1, 2, 16000, 512, 'NONE', 'not compressed')
            f.setparams(params)
            f.writeframes(struct.pack('h' * len(self.audio), *self.audio))

    def denirotalk(self):
        print("thinking of a witty response...")

        self.messages.append({"role": "user", "content": self.prompt})

        self.response = client.chat.completions.create(
            model='gpt-4',
            temperature=0.5,
            messages=self.messages
        )

        self.response = self.response.choices[0].message.content

        print(self.response)

    def transcribe(self):
        result = self.model.transcribe(self.file, fp16=False)
        self.prompt = result['text']
        return self.prompt

    def speak(self):
        pass
