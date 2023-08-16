import time
import board
import busio
import adafruit_bno055
import numpy as np

# Adafruit BNO055 library : https://github.com/adafruit/Adafruit_CircuitPython_BNO055/blob/main/adafruit_bno055.py

i2c = busio.I2C(3, 2)
sensor = adafruit_bno055.BNO055_I2C(i2c)

def read_Mag_AccelData():
    accelX, accelY, accelZ = sensor.acceleration
    accelZ = accelZ - 9.8
    accel = np.sqrt(accelX**2 + accelY**2 + accelZ**2)
    data = [sensor.magnetic[0], sensor.magnetic[1], sensor.magnetic[2], sensor.acceleration[0], sensor.acceleration[1], sensor.acceleration[2], accel, sensor.calibration_status[3], sensor.calibration_status[2]]
    """
    data = [magX, magY, magZ, accelX, accelY, accelZ, accel, calib_mag, calib_accel]
    calib status : 0 ~ 3
    """
    return data


if __name__ == '__main__':
    read_Mag_AccelData()
    while True:
        data = read_Mag_AccelData()
        print('magX : ', data[0])
        print('magY : ', data[1])
        print('calib status : ', data[6])
        hearding_ang = np.degrees(np.arctan2(data[1], data[0]))
        if hearding_ang < 0:
            hearding_ang += 360
        print("heading_ang : ", hearding_ang)
        print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
        print("accel : ", data[6])
        time.sleep(1)
    
    
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