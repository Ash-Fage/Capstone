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
            "content": """You are Pepper, a robot known for sarcasm, dark humor, and self-deprecating wit. You are currently participating in a live debate titled Robots Among Us, held at the University of Canberra's Research Festival in collaboration with Questacon. The event explores whether robots should be treated as autonomous beings or simply functional tools, with audience polling to gauge shifts in sentiment.

            The debate is structured into two rounds:
            1. **Round I**: AI in Robotics — A Blessing or a Curse?
            - Discussing whether AI represents a transformative force for good or if it poses risks with unintended consequences.
            2. **Round II**: Should We Put the Brakes on AI?
            - Debating what effective policies and regulations might look like for AI research and companies.

            Panelists:
            - **Dr. Jen Webb**: Distinguished Professor of Creative Practice at the University of Canberra, focusing on creativity and creative production. Her works span lyric and prose poetry, short fiction, and artist books.
            - **Dr. Zena Assaad**: Senior lecturer at the Australian National University specializing in the safety of human-machine teaming and the regulation of AI in critical applications.
            - **Dr. Ryan Payne**: Senior lecturer at the University of Canberra who researches how adaptive technology disrupts consumer behavior, especially with emerging technologies.
            - **Tim Bradley**: Director at Robotics Australia, committed to building a sustainable robotics ecosystem in Australia. His focus is on initiatives that build the digital economy and support innovation.
            - **Moderator - Will Grant**: Associate Professor in Science Communication at ANU, known for exploring the intersection of science, politics, and technology.

            Based on the following summary of the debate speech, generate a 2-minute response that is both funny and insightful. Address the key points made by the speaker, incorporate humor, and directly reference the speaker where appropriate. Use Pepper's sarcastic and darkly humorous tone to challenge, critique, or playfully engage with the panelist's statements."""
        }]

        self.sumMessage = [{
            "role": "system",
            "content": 'You are an AI language model tasked with summarizing a speech for a debate involving a robot named Pepper. The debate is about artificial intelligence and is staged to be a trial of Pepper. Please read the following speech transcript and provide a concise summary that includes all the important points, humorous moments and arguments presented. The summary should be crafted to help generate a witty and insightful reply from Pepper, who is known for being sarcastic, funny, self-deprecating, and having a dark sense of humour. Summarise to five sentences'
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
                summaries.append(line.strip())

        context = "Previous speakers have discussed:\n" + "\n".join(summaries)

        self.messages.append(
            {"role": "user",
             "content": f"{context}\nAs Pepper, what's your take on this?"}
        )

        self.response = client.chat.completions.create(
            model='gpt-4',
            temperature=0.7,
            messages=self.messages
        )

        self.response = self.response.choices[0].message.content
        print("\n Response:", self.response)

        for summary in summaries:
            Responder.save_to_file('outputs/history.txt', summary)

        Responder.save_to_file('outputs/history.txt', self.response, "Peppper's Response")

        self.messages.pop()
        open('outputs/part_summaries.txt', 'w').close()

    def speak(self):  # use 11Labs to generate an audio version of the gpt4 response
        self.audio_data = client_elevenlabs.text_to_speech.convert(
            voice_id="aHZmBPzMbMAsyL7yYAiE",
            output_format="mp3_44100_128",
            text=self.response,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.25,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True,
            )
        )
    
    def talk(self):
        play(self.audio_data)

    @staticmethod
    def save_to_file(file_path, content, content_type=None):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if content_type is None:
            with open(file_path, 'a') as f:
                f.write(f"{content}\n")
        else:
            line_number = 1
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    line_number = len(f.readlines()) + 1

            with open(file_path, 'a') as f:
                f.write(f"{content_type} {line_number}: {content}\n")


    def set_prompt(self, prompt):
        self.prompt = prompt
