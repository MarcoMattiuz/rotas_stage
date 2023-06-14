from adafruit_motor.servo import Servo

# Full dutycycle control limits
DUTY_LIMITS = (0, 19988)

class Motor:
    """
    Manage pwm controller and H bridge
    """

    def __init__(self, fwd: Servo, bwd: Servo):
        if fwd == bwd: raise ValueError("Pins must be different")

        if not isinstance(fwd, Servo) or not isinstance(bwd, Servo):
            raise ValueError('fwd and bwd must be adafruit_motor.servo.Servo objects')

        # Motor setup
        fwd.set_pulse_width_range(DUTY_LIMITS[0], DUTY_LIMITS[1])
        bwd.set_pulse_width_range(DUTY_LIMITS[0], DUTY_LIMITS[1])

        self.motors = {
            "forward": fwd,
            "backward": bwd
        }

    def power(self, power=None):
        powers = (0, 0)

        if power is None:
            return self.motors['forward'].fraction - self.motors['backward'].fraction
        elif power < 0:
            powers = (0, abs(power))
        elif power > 0:
            powers = (abs(power), 0)

        # La libreria di Adafruit è buggata... si va di 0.5 max
        self.motors["forward"].fraction = powers[0] * .5
        self.motors["backward"].fraction = powers[1] * .5

class MotorPair:
    """
    Manage motor pairs
    """

    def __init__(self, left: Motor, right: Motor) -> None:
        if not isinstance(left, Motor) or not isinstance(right, Motor):
            raise ValueError('fwd and bwd must be Motor() objects')
        self.left = left
        self.right = right

    def steerPower(self, steer = 0.0, power = 0.0):
        """
        Joystick control (steer = x axis, power = y axis)

        motor power map:

         0,1 ____1,1____ 1,0
            |     |     |
            |     |     |
        -1,1|----0,0----|1,-1
            |     |     |
            |_____|_____|
        0,-1    -1,-1    -1,0

        """

        def powermap(x):
            return 2*x + 1 if x < 0 else 1

        direction = steer > 0

        # powers = (power * steer, power) if direction else (power, power * steer)
        
        steer = 1 - abs(steer)
        
        powerInternal = abs(power) - 1 + powermap(power) * steer
        powerExternal = powermap(power) + (abs(power) - 1) * steer

        if direction:
            left = powerExternal
            right = powerInternal
        else:
            left = powerInternal
            right = powerExternal

        # print(f'\nleft: {left}\nright {right}\n')
        self.left.power(left)
        self.right.power(right)

    def leftPower(self, power = 0.0):
        self.left.power(power)

    def rightPower(self, power = 0.0):
        self.right.power(power)