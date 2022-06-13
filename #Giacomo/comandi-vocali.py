# pip install SpeechRecognition pyaudio
import os
from time import sleep
import speech_recognition as sr


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio, language="it-IT")
            # print(said)
        except Exception as e:
            # print("Exception: " + str(e))
            said = "non ho capito..."
    return said.lower()


def clear():
    os.system("cls")
    # os.system("clear")


WAKE = 'rover'

while True:
    text = get_audio()

    if text.count(WAKE) > 0:
        clear()
        print("Ti ascolto...")
        text = get_audio()
        print(text)