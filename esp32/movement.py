from machine import Pin, PWM

class Motor:
    """
    Manage H bridge
    """

    def __init__(self, fwd, bwd, freq = 50):
        if fwd == bwd: raise ValueError("Pins must be different")

        if not isinstance(fwd, Pin):
            fwd = Pin(int(fwd))
        if not isinstance(bwd, Pin):
            bwd = Pin(int(bwd))

        self.motors = {
            "forward": PWM(fwd, freq = freq, duty_u16 = 0),
            "backward": PWM(bwd, freq = freq, duty_u16 = 0)
        }

    def setpower(self, power=0):
        if power == 0:
            return {(name, mot.duty()) for name, mot in self.motors.items()}            
        elif power < 0:
            self.motors["forward"].duty(0)
            self.motors["backward"].duty(abs(power))
        else:
            self.motors["forward"].duty(abs(power))
            self.motors["backward"].duty(0)