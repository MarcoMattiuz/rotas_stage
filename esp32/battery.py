from machine import Pin, ADC
from led import RGB

R1 = 66700
R2 = 18000

VF = 0.6

VMAX = 15.0
VMIN = 11.0

class Battery(ADC):
    """
    Measures battery voltage through voltage divider
    """
    
    def __init__(self, pin, bits = 12, filter = 0.6, led: RGB = None) -> None:
        if not isinstance(pin, Pin):
            pin = Pin(int(pin))
        
        self.alpha = filter
        self.filter_val = 1
        self.indicator = led

        self.lvl = 0.0
        self.volts = 0.0

        super().__init__(pin)
        self.width(bits)
        self.atten(ADC.ATTN_11DB)

    def voltage(self):
        self.filter()
        self.volts = self.filter_val * (R1 + R2)/R2 + VF
        return round(self.volts)

    def level(self):
        vbat = self.voltage()
        self.lvl = round((vbat - VMIN) / (VMAX - VMIN), 2)
        self.limit(self.lvl)
        return self.lvl

    def width(self, bits = None):
        if bits is None: return self.bits
        else:
            self.bits = bits
            super().width(bits)

    def filter(self):
        vadc = self.read_uv() / 1000000
        self.filter_val = self.alpha * vadc + (1 - self.alpha) * self.filter_val
        return self.filter_val
    
    @staticmethod
    def limit(val, min = 0, max = 1):
        if min > max:
            min, max = (max, min)
        
        if val < min:
            val = min
        elif val > max:
            val = max
    
        return val
    
    def updateLed(self):
        self.level()
        if self.lvl > 0.8:
            self.indicator.color(RGB.BLUE)
        elif self.lvl < 0.3:
            self.indicator.color(RGB.RED)
        else:
            self.indicator.color(RGB.GREEN)