from machine import Pin, PWM, SoftI2C, UART
from ssd1306 import SSD1306_I2C
from battery import Battery
from movement import Motor

batt = Battery(36)

ser = UART(2, baudrate=115200, tx=17, rx=16)

gps = UART(1, baudrate=9600, rx=27)

leftMotor = Motor(32, 33)
rightMotor = Motor(25, 26)

display = SSD1306_I2C(128, 64, SoftI2C(sda=Pin(22), scl=Pin(23)))