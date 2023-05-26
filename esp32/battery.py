from machine import Pin, ADC

R1 = 66000
R2 = 18000

VMAX = 14.7
VMIN = 11.5

class Battery(ADC):
    """
    Measures battery voltage through voltage divider
    """
    
    def __init__(self, pin, bits = 12) -> None:
        if not isinstance(pin, Pin):
            pin = Pin(int(pin))
        super().__init__(pin)
        self.width(bits)

    def voltage(self):
        vadc = self.read_uv()/1000000
        return vadc * (R1 + R2)/R2

    def level(self):
        vadc = self.read_uv()/1000000
        vbat = vadc * (R1 + R2)/R2
        lvl = (vbat - VMIN) / (VMAX - VMIN)
        return lvl

    def width(self, bits = None):
        if bits is None: return self.bits
        else:
            self.bits = bits
            super().width(bits)