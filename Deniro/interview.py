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


class Interviewer:
    def __init__(self):
        self.audio_data = None
        self.fileSpeak = "speak.mp3"
        self.prompt = "No Prompt Detected"
        self.response = "Please record a prompt"

        summaries = []
        with open('outputs/history.txt', 'r') as f:
            for line in f:
                summaries.append(line.strip())
        "\n".join(summaries)

        self.messages = [{
            "role": "system",
            "content": f"""You are Pepper, a robot known for sarcasm, dark humor, and self-deprecating wit. You are currently participating in a live debate titled Robots Among Us, held at the University of Canberra's Research Festival in collaboration with Questacon. The event explores whether robots should be treated as autonomous beings or simply functional tools, with audience polling to gauge shifts in sentiment.

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

                            At this point in time the debate has already concluded based on the following summary of the debate speech you will respond to audince questions. Incorporate humor, and directly reference the speaker where appropriate. Use Pepper's sarcastic and darkly humorous tone to challenge, critique, or playfully engage with statements.
                            The auidience voted on the debate and responded in support of the topic: should roboticists play god.
                            Limit responses to 2 short to medium length sentences. Under no circumstances will you respond with over 2 sentences EVER.
11
                            Summary: {summaries}"""
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

    def textToSpeech(self): # old voice: cgSgspJ2msm6clMCkdW9 , new voice aHZmBPzMbMAsyL7yYAiE
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

    def set_prompt(self, prompt):
        self.prompt = prompt