import bno055
import GYSFDMAXB
from geographiclib.geodesic import Geodesic 
import math
import time
import logger
import motor


def cal_azimuth(lng1, lat1, lng2, lat2):
    lng1 = math.radians(lng1)
    lat1 = math.radians(lat1)
    lng2 = math.radians(lng2)
    lat2 = math.radians(lat2)
    dx = lng2 - lng1
    des_ang = 90 - math.degrees(math.atan2(math.cos(lat1)*math.tan(lat2)-math.sin(lat1)*math.cos(dx), math.sin(dx)))
    if des_ang < 0:
        des_ang += 360
    """
    https://keisan.casio.jp/exec/system/1257670779
    PointA(lng x1, lat y1), PointB(lng x2, lat y2)
            (gps_lng, gps_lat),     (des_lng, des_lat)
    ϕ = 90 - atan2(cosy1tany2 - siny1cosΔx, sinΔx)
    Δx = x2 - x1
    """
    return des_ang

def cal_distance(x1, y1, x2, y2):
    distance = Geodesic.WGS84.Inverse(y1, x1, y2, x2)['s12'] # [m]
    return distance

def cal_heading_ang(pre_gps, gps, err_mag):
    if err_mag != True:
        try:
            data = bno055.read_Mag_AccelData()
            """
            data = [magX, magY, magZ, accelX, accelY, accelZ, calib_mag, calib_accel]
            """
            hearding_ang = math.degrees(math.atan2(data[1], data[0]))
            if hearding_ang < 0:
                hearding_ang += 360
            return hearding_ang, data
        except:
            print("Error : Cant read Mag data")
            return 0, 0
    else:
        return cal_azimuth(pre_gps[0], pre_gps[1], gps[0], gps[1]), 0

def is_heading_goal(pre_gps, gps, des, err_mag):
    des_ang = cal_azimuth(gps[0], gps[1], des[0], des[1])
    heading_ang, data = cal_heading_ang(pre_gps, gps, err_mag)
    ang_diff = abs(des_ang - heading_ang)
    if ang_diff < 25 or 335 < ang_diff:
        return [des_ang, heading_ang, ang_diff, True, "Go Straight"] + gps + data
    else:
        if ((heading_ang > des_ang and ang_diff < 180) or (heading_ang < des_ang and ang_diff > 180)):
            return [des_ang, heading_ang, ang_diff, False, "Turn Left"] + gps + data
        else:
            return [des_ang, heading_ang, ang_diff, False, "Turn Right"] + gps + data

def is_stuck(pre_distance, later_distance):
    if abs(pre_distance - later_distance) < 0.1 and pre_distance != later_distance:
        return True
    else:
        return False

# Test destination point(lon, lat)
TEST_DESTINATION = [139.65489833333334, 35.95099166666667]

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