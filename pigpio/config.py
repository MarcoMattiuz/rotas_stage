from adafruit_servokit import ServoKit
from pigpio.movement import Motor, MotorPair
from pigpio.gps import GPS
from pigpio.led import RGB
import RPi.GPIO as io

_kit = ServoKit(channels=16, frequency=100)

channels = _kit.servo

gps = GPS(port = '/dev/ttyS0')

rightMotor = Motor(channels[1], channels[0])
leftMotor = Motor(channels[3], channels[2])

motors = MotorPair(leftMotor, rightMotor)

led = RGB(channels[4], channels[5], channels[6])

def reset_GPIO():
    for motor in channels: motor.angle = 0
    io.cleanup()