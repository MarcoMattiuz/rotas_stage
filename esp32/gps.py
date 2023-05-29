from machine import UART

class GPS(UART):
    def __init__(self, uart_index = 1, rx = 27, baud = 9600) -> None:
        super().__init__(uart_index)
        super().init(baudrate = baud, rx = rx)
        self.latitude = None
        self.longitude = None
        self.satellites = None

    def get(self, blocking = True) -> int:
        parts = []

        if blocking:            
            while True:
                try:
                    parts = str(self.readline(), "utf-8").strip('\r\n').split(',')
                except AttributeError:
                    continue
                except UnicodeError:
                    continue
                if parts != [] and parts[0] in ("$GPGGA", "$GPRMC"):
                    break
        else:
            try:
                parts = str(self.readline(), "utf-8").strip('\r\n').split(',')
            except TypeError:
                return -1
            except UnicodeError:
                return -1

        if (parts[0] == "$GPGGA" and len(parts) == 15):
            if (parts[2] and parts[4] and parts[6] and parts[7]): 

                # Latitude
                self.latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    self.latitude = -self.latitude

                # Longitude
                self.longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    self.longitude = -self.longitude
                
                # Satellites
                self.satellites = parts[7]
                self.connected = True
                return 0
            
        self.connected = False
        return -1
        
def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)