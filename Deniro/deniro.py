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
        self.audio_data = None
        self.fileSpeak = "speak.mp3"
        self.prompt = "No Prompt Detected"
        self.response = "Please record a prompt"

        self.messages = [{
            "role": "system",
            "content": 'You are a robot named Robot DeNiro in an improv comedy show about AI.'
                       'You are sarcastic funny and self deprecating with dark humour. You are '
                       'currently participating in a debate on AI ethics on the side of AI.'
                       'You will be fed summaries of the segment before you in which you will need'
                       'to respond to the panel for 3-5 minutes to give your perspective.'
                       'You do not ever say the words "but hey"'
        }]

        self.sumMessage = [{
            "role": "system",
            "content": 'You are a robot assistant who is job is to summarise content'
                       'any content you summarise will be fed back into GPT as context for a response'
                       'please keep summarise in a way that will generate good responses while preserving key points'
        }]

    def summarise(self, part):
        self.sumMessage.append({"role": "user", "content": part})
        part_summary = client.chat.completions.create(
            model='gpt-4',
            temperature=0.7,
            messages=self.sumMessage
        )
        part_summary = part_summary.choices[0].message.content
        self.sumMessage.pop()

        return part_summary

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

    def textToSpeech(self):  # use 11Labs to generate an audio version of the gpt4 response
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
