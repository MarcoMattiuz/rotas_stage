from adafruit_servokit import Servo

class RGB:
    """
    Manage RGB Leds
    """

    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    def __init__(self, red: Servo, green: Servo, blue: Servo) -> None:
        if not isinstance(red, Servo) or not isinstance(green, Servo) or not isinstance(blue, Servo):
            raise ValueError('colors must be adafruit_motor.servo.Servo() objects')
        
        self.r = red
        self.g = green
        self.b = blue

    def color(self, color = (0,0,0)) -> tuple:
        self.r.fraction = color[0]/255
        self.g.fraction = color[1]/255
        self.b.fraction = color[2]/255