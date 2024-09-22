import os
import whisper
import wave
import struct
from openai import OpenAI
from pvrecorder import PvRecorder
from pynput import keyboard
from elevenlabs import VoiceSettings, play
from elevenlabs.client import ElevenLabs


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

client_elevenlabs = ElevenLabs(
    api_key=os.environ.get("ELEVENLABS_API_KEY")
)


class Transcription:
    def __init__(self):
        self.recorder = PvRecorder(device_index=-1, frame_length=512)
        self.model = whisper.load_model('base.en')
        self.audio = []
        self.file = "record.wav"
        self.fileSpeak = "speak.mp3"
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

    def on_press(self, key):  # used to toggle recording status when shift is pressed
        if key == keyboard.Key.shift:
            if self.recording:
                self.recording = False
            else:
                self.recording = True

    def record(self):
        self.audio = []  # reset audio recording

        print("Press SHIFT to start and stop recording")

        with keyboard.Listener(on_press=self.on_press) as listener:  # creates a new  keyboard listener
            while True:  # loop will execute until some audio has been recorded
                if self.recording:
                    print("Recording...")
                    self.recorder.start()

                    while self.recording:  # will loop until shift is pressed and recording status changed
                        frame = self.recorder.read()  # reads audio frame from recorder
                        self.audio.extend(frame)  # adds audio frame to array

                    break

                if self.audio:  # terminates loop after any audio has been recorded
                    self.recorder.stop()
                    break

            listener.stop()  # terminates keyboard listener

        print("Recording Stopped\n")
        self.save()

    def save(self):  # used to save a recorded audio file in wav format
        with wave.open(self.file, 'wb') as f:
            params = (1, 2, 16000, 512, 'NONE', 'not compressed')
            f.setparams(params)
            f.writeframes(struct.pack('h' * len(self.audio), *self.audio))

    def denirotalk(self):  # utilise gpt4 chat completions api to generate deniro response
        print("thinking of a witty response...")

        self.messages.append({"role": "user", "content": self.prompt})

        self.response = client.chat.completions.create(
            model='gpt-4',
            temperature=0.5,
            messages=self.messages
        )

        self.response = self.response.choices[0].message.content

        print(self.response + "\n")

    def transcribe(self):  # utilises whisper to translate audio file to text
        result = self.model.transcribe(self.file, fp16=False)
        self.prompt = result['text']
        return self.prompt

    def speak(self):  # use 11Labs to generate an audio version of the gpt4 response
        speak = client_elevenlabs.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",
            output_format="mp3_22050_32",
            text=self.response,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            )
        )

        play(speak)
