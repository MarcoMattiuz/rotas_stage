from machine import Pin, ADC

R1 = 66700
R2 = 18000

VF = 0.6

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
        return round(self.filter_val * (R1 + R2)/R2, 2) + VF

    def level(self):
        vbat = self.voltage()
        lvl = round((vbat - VMIN) / (VMAX - VMIN), 2)
        return self.limit(lvl, 0, 1)

    def width(self, bits = None):
        if bits is None: return self.bits
        else:
            self.bits = bits
            super().width(bits)

    def filter(self):
        vadc = self.read_uv()/1000000
        self.filter_val = self.alpha * vadc + (1 - self.alpha) * self.filter_val
        return self.filter_val
    
    @staticmethod
    def limit(val, min, max):
        if min > max:
            min, max = (max, min)
        
        if val < min:
            val = min
        elif val > max:
            val = max
    
        return val