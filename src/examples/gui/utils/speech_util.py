
import win32com.client as win


class SpeechUtil:

    @staticmethod
    def speak_out():
        speak = win.Dispatch("SAPI.SpVoice")


if __name__ == "__main__":
    speak = win.Dispatch("SAPI.SpVoice")
    speak.rate = 5
    speak.Voice = speak.GetVoices().Item(0)
    print(speak.Voice.GetDescription())
    # speak.Voice = speak.GetVoices().Item(1)
    # print(speak.Voice.GetDescription())

    speak.Speak("Hello world")
