# Importing required modules
# importing pyttsx3
from email import message
import pyttsx3
# importing speech_recognition
import speech_recognition as sr
# importing os module
import os
from time import sleep
import pwmraspberry as pwm


# creating take_commands() function which
# can take some audio, Recognize and return
# if there are not any errors
def take_commands():
    # initializing speech_recognition
    r = sr.Recognizer()
    # opening physical microphone of computer
    with sr.Microphone() as source:
        print('Ascolto...')
        r.pause_threshold = 0.7
        # storing audio/sound to audio variable
        audio = r.listen(source, timeout=4)
        try:
            sleep(0.5)
            print("Riconoscimento...")
            # Recognizing audio using google api
            Query = r.recognize_google(audio, language='it')
            Query = Query.lower()
        except Exception as e:
            # returning none if there are errors
            return "none"
    # returning audio as text
    sleep(1)
    return Query


# creating Speak() function to giving Speaking power
# to our voice assistant
def Speak(audio):
    # initializing pyttsx3 module
    engine = pyttsx3.init()
    voice_id = 'italian'
    engine.setProperty('voice', voice_id)
    # anything we pass inside engine.say(),
    # will be spoken by our voice assistant
    sleep(0.5)
    engine.say(audio)
    engine.runAndWait()

Speak("Il rover è pronto")

v = 2
while True:
    command = take_commands()
    mess = ""
    if "none" in command:
        mess = "non ho capito"
    elif "avanti" in command:
        mess = "vado avanti"
        pwm.traz(v, 0)
    elif "indietro" in command:
        mess = "vado indietro"
        pwm.traz(-v, 0)
    elif "destra" in command:
        mess = "giro a destra"
        pwm.traz(v, 5)
        sleep(1)
        pwm.traz(v, 0)
    elif "sinistra" in command:
        mess = "giro a sinistra"
        pwm.traz(v, -5)
        sleep(1)
        pwm.traz(v, 0)
    elif "ferm" in command:
        mess = "sono fermo"
        pwm.traz(0,0)
    elif "interrompi" in command:
        exit()
    else:
        mess = "ho capito " + command
    print(mess)
    Speak(mess)
