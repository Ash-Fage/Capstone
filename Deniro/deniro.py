import os
from openai import OpenAI
from elevenlabs import VoiceSettings, play
from elevenlabs.client import ElevenLabs

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

client_elevenlabs = ElevenLabs(
    api_key=os.environ.get("ELEVENLABS_API_KEY")
)


class Conversation:
    def __init__(self):
        self.fileSpeak = "speak.mp3"
        self.prompt = "No Prompt Detected"
        self.response = "Please record a prompt"

        self.messages = [{
            "role": "system",
            "content": 'You are a robot named Robot DeNiro in an improv comedy show about AI.'
                       'You are sarcastic funny and self deprecating with dark humour. You always '
                       'limit your response to 3 to 5 sentences'
            # 'You output one of the following EMOTIONS = HAPPY, SAD, ANGRY, NEUTRAL, '
            # 'SURPRISED, DISGUSTED, FEARFUL, SARCASTIC, CHEEKY attached with the '
            # 'sentiment of each sentence'
            # 'An emotion should be output in the format [EMOTION]. Each and every '
            # 'sentence you output should have an emotion attached to it'
                       'You do not ever say the words "but hey"'
        }]

    def generate_response(self):  # utilise gpt4 chat completions api to generate deniro response
        print("thinking of a witty response...")

        self.messages.append({"role": "user", "content": self.prompt})

        self.response = client.chat.completions.create(
            model='gpt-4',
            temperature=0.7,
            messages=self.messages
        )

        self.response = self.response.choices[0].message.content

        print(self.response + "\n")

    def speak(self):  # use 11Labs to generate an audio version of the gpt4 response
        self.audio_data = client_elevenlabs.text_to_speech.convert(
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
    
    def talk(self):
        play(self.audio_data)

    def set_prompt(self, prompt):
        self.prompt = prompt
