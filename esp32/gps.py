from machine import UART

class GPS(UART):
    buff = bytearray(255)

    def __init__(self, uart_index = 1, rx = 27, baud = 9600) -> None:
        super().__init__(uart_index, rx = rx, baudrate = baud)
        self.latitude = None
        self.longitude = None
        self.satellites = None

    def getGPS(self, blocking = True):
        if blocking:
            while self.buff == '':
                # self.readline()
                self.buff = str(self.readline(), 'utf-8')
                parts = self.buff.split(',')
        else:
            self.buff = str(self.readline(), 'utf-8')
            parts = self.buff.split(',')
    
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]): 

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
        else:
            self.connected = False
            return -1
        
def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)