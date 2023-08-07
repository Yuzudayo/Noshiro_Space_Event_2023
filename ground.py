import bno055
import GYSFDMAXB
from geographiclib.geodesic import Geodesic 
import math
import time
import logger
import motor

DES_LNG = 139.65489833333334
DES_LAT = 35.95099166666667

#TODO : 2地点入力できるようにする
#TODO : ライブラリを用いて計算する
def cal2pos_ang(gps_lng, gps_lat):
    des_lng = math.radians(DES_LNG)
    des_lat = math.radians(DES_LAT)
    dx = des_lng - gps_lng
    des_ang = 90 - math.degrees(math.atan2(math.cos(gps_lat)*math.tan(des_lat)-math.sin(gps_lat)*math.cos(dx), math.sin(dx)))
    print("To destination angle : ", des_ang)
    return des_ang

def cal_distance(x2, y2):
    while GYSFDMAXB.read_GPSData() == [0,0]:
        print("Waiting for GPS reception")
        time.sleep(5)
    gps = GYSFDMAXB.read_GPSData()
    distance = Geodesic.WGS84.Inverse(gps[1], gps[0], y2, x2)['s12'] # [m]
    return distance

#TODO : 地磁気センサの値によって場合分け
def cal_heading_ang(err_mag):
    if err_mag != True:
        data = bno055.read_Mag_AccelData()
        """
        data = [magX, magY, magZ, accelX, accelY, accelZ, calib_mag, calib_accel]
        """
        hearding_ang = math.atan2(data[1], data[0])
        hearding_ang = math.degrees(hearding_ang)
        if hearding_ang < 0:
            hearding_ang += 360
        print("Heading angle :",hearding_ang)
        return hearding_ang, data
    else:
        

def is_heading_goal():
    while GYSFDMAXB.read_GPSData() == [0,0]:
        print("Waiting for GPS reception")
        time.sleep(5)
    gps = GYSFDMAXB.read_GPSData()
    gps_lng = math.radians(gps[0])
    gps_lat = math.radians(gps[1])
    To_des_ang = cal2des_ang(gps_lng, gps_lat)
    heading_ang, data = cal_heading_ang()
    ang_diff = abs(To_des_ang - heading_ang)
    if ang_diff < 25 or 335 < ang_diff:
        return [To_des_ang, heading_ang, ang_diff, True, "Go Straight"] + gps + data
    else:
        if ((heading_ang > To_des_ang and ang_diff < 180) or (heading_ang < To_des_ang and ang_diff > 180)):
            return [To_des_ang, heading_ang, ang_diff, False, "Turn Left"] + gps + data
        else:
            return [To_des_ang, heading_ang, ang_diff, False, "Turn Right"] + gps + data

if __name__ == '__main__':
    ground_log = logger.GroundLogger()
    logger.GroundLogger.state = 'Normal'
    drive = motor.Motor()
    while True:
        distance = cal_distance(DES_LNG, DES_LAT)
        print("distance :", distance)
        if distance < 3:
            print("end")
            drive.stop()
            ground_log.end_of_ground_phase()
            break
        time.sleep(0.2)
        data = is_heading_goal()
        ground_log.ground_logger(data, distance)
        if data[3] == True:
            print("Heading Goal!!")
            # drive.forward()
        else:
            if data[4] == 'Turn Right':
                print("Turn right")
                # drive.turn_right()
            elif data[4] == 'Turn Left':
                print("Turn left")
                # drive.turn_left()
        time.sleep(0.8)