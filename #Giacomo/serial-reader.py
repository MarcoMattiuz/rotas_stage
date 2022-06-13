import serial
from time import sleep

arduino = serial.Serial(port='COM12', baudrate=9600)

try:
    while 1:
        mess = arduino.readline().decode()
        mess = mess[-4:-2]
        # print(mess)

        if int(mess) < 15:
            print ("stop")

except (KeyboardInterrupt):
    arduino.close()