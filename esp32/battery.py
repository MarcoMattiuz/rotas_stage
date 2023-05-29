from machine import Pin, ADC

R1 = 66000
R2 = 18000

VMAX = 14.7
VMIN = 11.5

class Battery(ADC):
    """
    Measures battery voltage through voltage divider
    """
    
    def __init__(self, pin, bits = 12, filter = 0.6) -> None:
        if not isinstance(pin, Pin):
            pin = Pin(int(pin))
        self.alpha = filter
        self.filter_val = 1

        super().__init__(pin)
        self.width(bits)
        self.atten(ADC.ATTN_11DB)

    def voltage(self):
        self.filter()
        return self.filter_val * (R1 + R2)/R2

    def level(self):
        vbat = self.voltage()
        lvl = (vbat - VMIN) / (VMAX - VMIN)
        return lvl

    def width(self, bits = None):
        if bits is None: return self.bits
        else:
            self.bits = bits
            super().width(bits)

    def filter(self):
        vadc = self.read_uv()/1000000
        self.filter_val = self.alpha * vadc + (1 - self.alpha) * self.filter_val
        return self.filter_val