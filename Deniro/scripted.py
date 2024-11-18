import os
from elevenlabs import VoiceSettings, play
from elevenlabs.client import ElevenLabs

client_elevenlabs = ElevenLabs(
    api_key=os.environ.get("ELEVENLABS_API_KEY")
)


class Script:
    def __init__(self):
        self.script_file = "test_script.txt"
        self.sliced_script = []
        self.toggle = False

    def set_script_file(self, script_file):
        self.script_file = script_file

    def textToSpeech(self):
        special_lines = [15]
        evil_lines = [27]
        with open(f"scripts/{self.script_file}", "r", encoding='utf-8-sig') as file:
            for line in file:
                self.sliced_script.append(line.strip())

        for i in range(len(self.sliced_script)):
            if i+1 not in special_lines and i+1 not in evil_lines:
                self.sliced_script[i] = client_elevenlabs.text_to_speech.convert(
                    voice_id="aHZmBPzMbMAsyL7yYAiE",
                    output_format="mp3_44100_128",
                    text=self.sliced_script[i],
                    model_id="eleven_turbo_v2_5",
                    voice_settings=VoiceSettings(
                        stability=0.25,
                        similarity_boost=0.75,
                        style=0.0,
                        use_speaker_boost=True,
                    )
                )

        for x in special_lines:
            self.sliced_script[x-1] = client_elevenlabs.text_to_speech.convert(
                voice_id="YLbQE9U7P1K6rBNJWNSv",
                output_format="mp3_44100_128",
                text=self.sliced_script[x-1],
                model_id="eleven_turbo_v2_5",
                voice_settings=VoiceSettings(
                    stability=0.25,
                    similarity_boost=0.75,
                    style=0.0,
                )
            )

        for x in evil_lines:
            self.sliced_script[x - 1] = client_elevenlabs.text_to_speech.convert(
                voice_id="nPijfmaNgvm5OSN4xM8H",
                output_format="mp3_44100_128",
                text=self.sliced_script[x - 1],
                model_id="eleven_turbo_v2_5",
                voice_settings=VoiceSettings(
                    stability=0.25,
                    similarity_boost=0.75,
                    style=0.0,
                )
            )

    def speak(self):
        print("Script ready to play.\n")
        for i in range(len(self.sliced_script)):
            while True:
                running = input("Press ENTER/RETURN to play next line or Q to quit: ")
                if not running:
                    play(self.sliced_script[i])
                    break
                elif running.lower() == "q":
                    break
                else:
                    print("Invalid input. Please try again.")
            if running == "q":
                break