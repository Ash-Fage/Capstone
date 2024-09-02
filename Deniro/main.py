from transcription import Transcription


def main():
    test = Transcription()

    while True:
        test.record()
        print(test.transcribe().strip(), "\n")


if __name__ == '__main__':
    main()
