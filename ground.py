import bno055
import GYSFDMAXB
from geographiclib.geodesic import Geodesic 
import math
import time
import logger
import motor

des_lng = 139.65497333333334
des_lat = 35.950936666666664

def cal2des_ang(gps_lng, gps_lat):
    des_ang = Geodesic.WGS84.Inverse(gps_lat, gps_lng, des_lat, des_lng)['a12']
    print("To destination angle :", des_ang)
    return des_ang

def cal_distance(x2, y2):
    while GYSFDMAXB.read_GPSData() == [0,0]:
        print("Waiting for GPS reception")
        time.sleep(5)
    gps = GYSFDMAXB.read_GPSData()
    distance = Geodesic.WGS84.Inverse(gps[1], gps[0], y2, x2)['s12'] # [m]
    return distance

def cal_heading_ang():
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
    if ang_diff < 20 or 340 < ang_diff:
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
        distance = cal_distance(des_lng, des_lat)
        print("distance :", distance)
        if distance < 3:
            print("end")
            drive.stop()
            ground_log.end_of_ground_phase()
            break
        data = is_heading_goal()
        ground_log.ground_logger(data, distance)
        if data[3] == True:
            print("Heading Goal!!")
            drive.forward()
        else:
            if data[4] == 'Turn Right':
                print("Turn right")
                drive.turn_right()
            elif data[4] == 'Turn Left':
                print("Turn left")
                drive.turn_left()
        time.sleep(0.8)