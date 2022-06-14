import speech_recognition as sr
from time import sleep
import pwmraspberry as pwm
import os


def clear():
    # os.system("cls")
    os.system("clear")


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("->")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio, language="it-IT")
            # print(said)
        except Exception as e:
            # print("Exception: " + str(e))
            said = "none"
            pass
    return said.lower()


print("Il rover è pronto")

v = 2
while True:

    command = get_audio()
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
        sleep(1.5)
        pwm.traz(v, 0)
    elif "sinistra" in command:
        mess = "giro a sinistra"
        pwm.traz(v, -5)
        sleep(1.5)
        pwm.traz(v, 0)
    elif "girotondo" in command:
        pwm.traz(v, 5)
        sleep(5)
        pwm.traz(0, 0)
    elif "ferm" in command:
        mess = "sono fermo"
        pwm.traz(0,0)
    elif "interromp" in command:
        exit()
    else:
        mess = "ho capito: " + command
