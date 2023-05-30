from machine import Pin, PWM, SoftI2C, UART
from ssd1306 import SSD1306_I2C
from battery import Battery
from movement import Motor
from gps import GPS

batt = Battery(4)

ser = UART(2, baudrate=115200, tx=17, rx=16)

gps = GPS()

leftMotor = Motor(32, 33)
rightMotor = Motor(25, 26)

display = SSD1306_I2C(128, 64, SoftI2C(sda=Pin(22), scl=Pin(23)))