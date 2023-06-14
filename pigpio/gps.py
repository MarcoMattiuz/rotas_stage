from serial import Serial

class GPS(Serial):
    def __init__(self, port: str, baud = 9600) -> None:
        super().__init__(port = port, baudrate=baud)
        
        self.latitude = None
        self.longitude = None
        self.satellites = 0
        self.speed = 0

    def get(self) -> int:
        parts = []

        while True:
            try:
                parts = str(self.readline(), "utf-8").strip('\r\n').split(',')
            except AttributeError:
                continue
            except UnicodeError:
                continue
            except TypeError:
                continue
            if parts != [] and parts[0] in ("$GPGGA", "$GPRMC"):
                break
        
        if (parts[0] == "$GPGGA" and len(parts) == 15 and parts[2] and parts[4] and parts[7]):
            try:
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
                
            except ValueError:
                return -1
            except IndexError:
                return -1
            
            return 0
        
        if (parts[0] == '$GPRMC'):
            try:
                # Latitude
                self.latitude = convertToDegree(parts[3])
                if not isinstance(self.latitude, str): return -1
                if (parts[4] == 'S'):
                    self.latitude = -self.latitude
                
                # Longitude
                self.longitude = convertToDegree(parts[5])
                if not isinstance(self.longitude, str): return -1
                if (parts[6] == 'W'):
                    self.longitude = -self.longitude

                # Speed
                self.speed = float(parts[7]) * 1.852
            
            except ValueError:
                return -1
            except IndexError:
                return -1
            
        self.connected = False
        return -1
        
def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100)
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)