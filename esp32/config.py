from machine import Pin, SoftI2C, UART
from ssd1306 import SSD1306_I2C
from battery import Battery
from movement import Motor, MotorPair
from gps import GPS
from led import RGB

BROADCAST_RATE = 3000   # [ms]

led = RGB(0, 2, 15)

batt = Battery(12, filter = 0.2, led = led)

ser = UART(2, baudrate=115200, tx=17, rx=16)

gps = GPS(rx = 13)

leftMotor = Motor(33, 32)
rightMotor = Motor(26, 25)

motors = MotorPair(leftMotor, rightMotor)

# display = SSD1306_I2C(128, 64, SoftI2C(sda=Pin(22), scl=Pin(23)))