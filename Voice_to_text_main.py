
import speech_recognition as sr
import pyttsx3
import sys

r = sr.Recognizer()



def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
while (1):

    try:

        with sr.Microphone() as source2:

    
            r.adjust_for_ambient_noise(source2, duration=0.2)

            audio2 = r.listen(source2)

            NoteText = r.recognize_google(audio2)
            NoteText = NoteText.lower()

            with open('output.txt','a') as f:
                print(NoteText, file=f)

            print(NoteText)
            SpeakText(NoteText)



    except sr.RequestError as e:
        print("Could not return results; {0}".format(e))

    except sr.UnknownValueError:
        print("problem")
