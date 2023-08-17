import serial
import micropyGPS
import threading
import time

gps = micropyGPS.MicropyGPS(9, 'dd') # The arguments are the time zone offset and the output format

def rungps(): # Read the GPS module and update the GPS object
    try:
        uart = serial.Serial('/dev/serial0', 9600, timeout=10)
        uart.readline() # Discard the first line because it can read half-baked data
        while True:
            sentence = uart.readline().decode('utf-8') # Read GPS data and convert to string
            if sentence[0] != '$': # Throw away if it doesn't start with '$'
                continue
            for x in sentence: # Parse the read string and add/update data to the GPS object
                gps.update(x)
    except:
        pass

gpsthread = threading.Thread(target=rungps, args=())
gpsthread.daemon = True
gpsthread.start()

def read_GPSData():
    if gps.clean_sentences > 20: # Output when proper data accumulates to some extent
        gps_data = [gps.longitude[0], gps.latitude[0]]
        return gps_data
    else:
        return [0, 0]
    
if __name__ == '__main__':
    while True:
        data = read_GPSData()
        print('longitude : ', data[0], 'latitude : ', data[1])
        time.sleep(1)