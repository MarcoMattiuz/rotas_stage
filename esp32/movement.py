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

    def power(self, power=None):
        powers = (0, 0)
        if power is None:
            # Old:
            # return {(name, mot.duty()) for name, mot in self.motors.items()}

            return self.motors['forward'].duty() - self.motors['backward'].duty()
        
        elif power < 0:
            powers = (0, abs(power))
        elif power > 0:
            powers = (abs(power), 0)

        self.motors["forward"].duty(powers[0])
        self.motors["backward"].duty(powers[1])

    async def asyncPower(self, power=None):
        powers = (0, 0)
        if power is None:
            return self.motors['forward'].duty() - self.motors['backward'].duty()
        elif power < 0:
            powers = (0, abs(power))
        elif power > 0:
            powers = (abs(power), 0)

        self.motors["forward"].duty(powers[0])
        self.motors["backward"].duty(powers[1])

class MotorPair:
    def __init__(self, left: Motor, right: Motor) -> None:
        self.left = left
        self.right = right

    async def steerPower(self, steer = 0.0, power = 0.0):
        direction = steer < 0

        steer = 1 - abs(steer)

        powers = (power * steer, power) if direction else (power, power * steer)

        self.left.power(powers[0])
        self.right.power(powers[1])

    def leftPower(self, power = 0.0):
        self.left.power(power)

    def rightPower(self, power = 0.0):
        self.right.power(power)