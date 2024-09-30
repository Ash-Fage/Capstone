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
        with open(f"scripts/{self.script_file}", "r", encoding='utf-8-sig') as file:
            for line in file:
                self.sliced_script.append(line.strip())

        for i in range(len(self.sliced_script)):
            self.sliced_script[i] = client_elevenlabs.text_to_speech.convert(
                voice_id="pNInz6obpgDQGcFmaJgB",
                output_format="mp3_22050_32",
                text=self.sliced_script[i],
                model_id="eleven_turbo_v2_5",
                voice_settings=VoiceSettings(
                    stability=0.0,
                    similarity_boost=1.0,
                    style=0.0,
                    use_speaker_boost=True,
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
