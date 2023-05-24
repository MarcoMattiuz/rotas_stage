import json
from serial import Serial

class BoardCOM(Serial):
    def __init__(self, pwm_bits: int = 8, port: str = None, baudrate: int = 9600, bytesize: int = 8, parity: str = "N", stopbits: float = 1, timeout: float = None, xonxoff: bool = False, rtscts: bool = False, write_timeout: float = None, dsrdtr: bool = False, inter_byte_timeout: float = None, exclusive: float = None) -> None:
        super().__init__(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, write_timeout, dsrdtr, inter_byte_timeout, exclusive)

        self.pwmbits = pwm_bits

    @staticmethod
    def prop(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def _traz_old(self, velocita, sterzo):
        if sterzo < 0:
            sterzo = -sterzo
            v_dx = velocita
            v_sx = self.prop(sterzo, 0, 5, velocita, -velocita)
        else:
            v_dx = self.prop(sterzo, 0, 5, velocita, -velocita)
            v_sx = velocita

        if v_dx < 0:
            v_dx = -v_dx
            v_dx = self.prop(v_dx, 0, 5, 0, 100)
            # right1.ChangeDutyCycle(0)
            # right2.ChangeDutyCycle(v_dx)
        else:
            v_dx = self.prop(v_dx, 0, 5, 0, 100)
            # right1.ChangeDutyCycle(v_dx)
            # right2.ChangeDutyCycle(0)

        if v_sx < 0:
            v_sx = -v_sx
            v_sx = self.prop(v_sx, 0, 5, 0, 100)
            # left1.ChangeDutyCycle(0)
            # left2.ChangeDutyCycle(v_sx)
        else:
            v_sx = self.prop(v_sx, 0, 5, 0, 100)
            # left1.ChangeDutyCycle(v_sx)
            # left2.ChangeDutyCycle(0)

    @staticmethod
    def limit(val, min = 0, max = 255):
        """
        Limits val to the defined range. Defaults are uint8_t vals
        """

        if max < min: max, min = min, max
        return max if val > max else min if val < min else val
    
    def send_power(self, left: float, right: float):
        """
        left e right: float 0:1
        Passa interi senza segno alla scheda
        """

        left = self.prop(left, 0, 1, 0, self.pwmbits)
        right = self.prop(right, 0, 1, 0, self.pwmbits)

        if self.is_open:
            self.write(json.dumps({'left': int(left), 'right': int(right)}).encode())

    def steer(self, speed, steer):
        """
        Input processing
        """
        
        direction = steer < 0

        steer = 1 - abs(steer)

        if direction:
            right = speed
            left = speed * steer
        else:
            right = speed * steer
            left = speed

        self.send_power(left, right)

        return left, right

if __name__ == '__main__':
    a = BoardCOM(pwm_bits=10, port='/dev/ttyACM0', baudrate=115200)
    data = ''

    while data == b'':
        a.write(bytes(1))
        data = a.readline()

    a.send_power(0.3, 0.6)