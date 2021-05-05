import speech_recognition as sr
import pyttsx3 as reader

s = reader.init()
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak Anything:")
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        s.say(text)
        s.runAndWait()
    except:
        print("Sorry couldn't recognize your voice")