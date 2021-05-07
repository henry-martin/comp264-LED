import speech_recognition as sr
import pyttsx3
import sys

r = sr.Recognizer()


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def Notes():
    try:

        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            SpeakText("Please say your note")
            audio2 = r.listen(source2)

            # Using ggogle to recognize audio
            NoteText = r.recognize_google(audio2)
            NoteText = NoteText.lower()

            with open('output.txt','a') as f:
                print(NoteText, file=f)

            print(NoteText)
            NoteText += ". End of notes"
            SpeakText(NoteText)

            #sourceFile = open('demo.txt', 'w')
            #print("Did you say " + MyText)
            #sourceFile.close()

    except sr.RequestError as e:
        print("Could not return results; {0}".format(e))

    except sr.UnknownValueError:
        print("problem")

    return
