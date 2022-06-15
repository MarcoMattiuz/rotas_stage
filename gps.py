import serial
import os, sys, stat

os.system("sudo chmod 777 /dev/ttyS0")
s = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
)

while 1:
    mess = s.read().decode()
    print(mess, end='')

