import time
import board
import adafruit_bno055
import datetime
import csv

# Adafruit BNO055 library : https://github.com/adafruit/Adafruit_CircuitPython_BNO055/blob/main/adafruit_bno055.py

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

def read_Mag_AccelData():
    data = [sensor.magnetic[0], sensor.magnetic[1], sensor.magnetic[2], sensor.acceleration[0], sensor.acceleration[1], sensor.acceleration[2], sensor.calibration_status[3], sensor.calibration_status[2]]
    """
    data = [magX, magY, magZ, accelX, accelY, accelZ, calib_mag, calib_accel]
    calib status : 0 ~ 3
    """
    print(data)
    return data

if __name__ == '__main__':
    now = datetime.datetime.now()
    filename = 'pressure/' + now.strftime('%Y%m%d_%H%M%S') + '_pressure.csv'
    read_Mag_AccelData()
    while True:
        data = read_Mag_AccelData()
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([data[0], data[1], data[6]])
            print('magX : ', data[0])
            print('magY : ', data[1])
            print('calib status : ', data[6])
            f.close()
        time.sleep(0.1)
    
    
    # while True:
    #     print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    #     print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    #     print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    #     print("Euler angle: {}".format(sensor.euler))
    #     print("Quaternion: {}".format(sensor.quaternion))
    #     print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    #     print("Gravity (m/s^2): {}".format(sensor.gravity))
    #     print()
    #     time.sleep(1)

        