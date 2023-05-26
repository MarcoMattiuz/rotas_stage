from machine import Pin, PWM, SoftI2C, UART
import ssd1306

ser = UART(2, baudrate=115200, tx=17, rx=16)

leftMotor = PWM(Pin(18), freq=50, duty_u16=0)
rightMotor = PWM(Pin(19), freq=50, duty_u16=0)

class Motor:
    """
    Manage H bridge
    """

    def __init__(self, fwd, bwd, freq = 50):
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
            self.motors["forward"].duty(abs(power))





OledSDA = Pin(22)
OledSCL = Pin(23)

display = ssd1306.SSD1306_I2C(128, 64, SoftI2C(sda=OledSDA, scl=OledSCL))