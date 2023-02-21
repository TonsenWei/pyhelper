import win32com.client as win

def word_pronunciation():
    speak = win.Dispatch("SAPI.SpVoice")
    
    speak.Speak("come on, baby!")
    speak.Speak("宝贝儿，你好!")

if __name__ == "__main__":
    word_pronunciation()