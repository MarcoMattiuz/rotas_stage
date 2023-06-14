from machine import PWM, Pin

class RGB:
    """
    Manage RGB Leds
    """

    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    def __init__(self, rpin, gpin, bpin, freq = 100) -> None:
        if not isinstance(rpin, Pin):
            rpin = Pin(int(rpin))
        if not isinstance(gpin, Pin):
            gpin = Pin(int(gpin))
        if not isinstance(bpin, Pin):
            bpin = Pin(int(bpin))

        self.r = PWM(rpin, freq = freq, duty_u16 = 0)
        self.g = PWM(gpin, freq = freq, duty_u16 = 0)
        self.b = PWM(bpin, freq = freq, duty_u16 = 0)

    def color(self, color: tuple = ()) -> tuple:
        if color != ():
            self.r.duty(color[0]*4)
            self.g.duty(color[1]*4)
            self.b.duty(color[2]*4)
        else:
            return (self.r.duty(), self.g.duty(), self.b.duty())