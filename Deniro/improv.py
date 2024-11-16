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


class Responder:
    def __init__(self):
        self.audio_data = None
        self.prompt = "No prompt detected"
        self.response = "Please record a prompt"

        self.messages = [{
            "role": "system",
            "content": 'You are a robot named Robot DeNiro in an improv comedy show about AI.'
                       'You are sarcastic funny and self deprecating with dark humour. You are '
                       'currently participating in a debate on AI ethics on the side of AI.'
                       'You will be fed summaries of the segment before you in which you will reply'
                       'You will limit responses to 2 sentences.'
                       'You do not ever say the words "but hey"'
        }]

        self.sumMessage = [{
            "role": "system",
            "content": 'You are a robot assistant who is job is to summarise content'
                       'You will be fed content from a human speaker which you will then summarise'
                       'any content you summarise will be fed back into GPT as context for a response'
                       'please keep summarise in a way that will generate good responses while preserving key points'
        }]

    def summarise(self):
        file_path = 'outputs/part_summaries.txt'

        self.sumMessage.append({"role": "user", "content": self.prompt})
        part_summary = client.chat.completions.create(
            model='gpt-4',
            temperature=0.7,
            messages=self.sumMessage
        )
        part_summary = part_summary.choices[0].message.content

        Responder.save_to_file(file_path, part_summary, "Summary")
        self.sumMessage.pop()

    def respond(self):
        summaries = []

        with open('outputs/part_summaries.txt', 'r') as f:
            for line in f:
                content = ": ".join(line.strip().split(": ")[1:])
                summaries.append(content)

        context = "Previous speakers have discussed:\n" + "\n".join(summaries)

        self.messages.append(
            {"role": "user",
             "content": f"{context}\nAs Robot DeNiro, what's your take on this?"}
        )

        self.response = client.chat.completions.create(
            model='gpt-4',
            temperature=0.7,
            messages=self.messages
        )

        self.response = self.response.choices[0].message.content
        print("\n Response:", self.response)

        for summary in summaries:
            Responder.save_to_file('outputs/history.txt', summary, "Summary")

        Responder.save_to_file('outputs/history.txt', self.response, "Response")

        self.messages.pop()
        open('outputs/part_summaries.txt', 'w').close()

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

        play(self.audio_data)

    @staticmethod
    def save_to_file(file_path, content, content_type):
        line_number = 1
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                line_number = len(f.readlines()) + 1

        with open(file_path, 'a') as f:
            f.write(f"{content_type} {line_number}: {content}\n")

    def set_prompt(self, prompt):
        self.prompt = prompt
