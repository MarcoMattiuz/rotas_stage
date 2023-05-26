from time import sleep
import ujson
from config import *


def get_data() -> str:
    data = None
    while data == None:
        try:
            data = ser.readline().decode()
        except AttributeError:
            sleep(0.1)
    return data

def mainloop():
    # get data from serial
    data = get_data()
    
    # parse json
    doc = ujson.loads(data)
    left = int(doc["left"])
    right = int(doc["right"])
    oled = doc["oled"]
    
    # activate motors/display
    LeftMotor.duty(left)
    RightMotor.duty(right)

    display.fill(0)
    display.text(oled, 0, 0, 1)
    display.show()

while True:
    try:
        mainloop()
    except:
        break