"""
    NOSHIRO SPACE EVENT 2023
    ASTRUM MAIN PROGRAM
    
    Author : Yuzu
    Language : Python Ver.3.9.2
    Last Update : 08/08/2023
"""

import GYSFDMAXB
import motor
import ground
import floating
import img_proc
import logger
import time

# destination point(lon, lat)
DESTINATION = [139.65489833333334, 35.95099166666667]


print("Hello World!!")
error_log = logger.ErrorLogger()
drive = motor.Motor()
drive.stop()

"""
Floating Phase
"""
phase = 1
print("phase : ", phase)
floating_log = logger.FloatingLogger()
"""
state Rising
      Falling
      Landing
      Error
"""
state = 'Rising'
floating_log.state = 'Rising'
start = time.time()
init_altitude = 0
data = floating.cal_altitude(init_altitude)
init_altitude = data[2]
print("initial altitude : {}." .format(init_altitude))
floating_log.floating_logger(data)
print("Rising phase")
while phase == 1:
    while state == 'Rising':
        data = floating.cal_altitude(init_altitude)
        altitude = data[2]
        floating_log.floating_logger(data)
        print("Rising")
        # Incorrect sensor value
        if altitude < -5:
            state = 'Error'
            error_log.baro_error_logger(phase, data)
            print("Error")
        if altitude >= 6:
            state = 'Ascent Completed'
            floating_log.state = 'Ascent Completed'
        now = time.time()
        if now - start > 900:
            print('5 minutes passed')
            state = 'Landing'
            floating_log.state = 'Landing'
            floating_log.end_of_floating_phase('Landing judgment by passage of time.')
            break
        print("altitude : {}." .format(altitude))
        time.sleep(1.5)
    while state == 'Ascent Completed':
        data = floating.cal_altitude(init_altitude)
        altitude = data[2]
        floating_log.floating_logger(data)
        print("Falling")
        if altitude <= 3:
            state = 'Landing'
            floating_log.state = 'Landing'
            floating_log.end_of_floating_phase()
        now = time.time()
        if now - start > 900:
            print('5 minutes passed')
            state = 'Landing'
            floating_log.state = 'Landing'
            floating_log.end_of_floating_phase('Landing judgment by passage of time.')
            break
        print("altitude : {}." .format(altitude))
        time.sleep(0.2)
    while state == 'Error':
        now = time.time()
        if now - start > 900:
            print('5 minutes passed')
            state = 'Landing'
            floating_log.state = 'Landing'
            floating_log.end_of_floating_phase('Landing judgment by passage of time.')
            break
        time.sleep(1)
    print("Landing")
    time.sleep(5)
    drive.servo() # Separation mechanism activated
    break

reach_goal = False
error_mag = False
while not reach_goal:
    """
    Ground Phase
    """
    phase = 2
    print("phase : ", phase)
    ground_log = logger.GroundLogger()
    ground_log.state = 'Normal'
    while GYSFDMAXB.read_GPSData() == [0,0]:
            print("Waiting for GPS reception")
            time.sleep(5)
    gps = GYSFDMAXB.read_GPSData()
    data = ground.is_heading_goal(gps, DESTINATION, [0,0], error_mag)
    pre_distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
    ground_log.ground_logger(data, pre_distance)
    while phase == 2:
        count = 0
        while data[3] != True: # Not heading the goal
            count += 1
            # Abnormal geomagnetic sensor
            if count >= 20:
                error_mag = True
                ground_log.state = 'Error Mag'
                break
            # Check if the position is normal
            if count % 10 == 0:
                stuck = ground.is_stuck(pre_distance, distance)
                # Stuck Processing
                if stuck:
                    ground_log.state = 'Stuck'
                    ground_log.stuck_err_logger(pre_distance, distance, abs(distance - pre_distance))
                    print('stuck')
                    drive.stuck()
                    pre_gps = gps
                    gps = GYSFDMAXB.read_GPSData()
                    pre_distance = distance
                    distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
                    data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
                    ground_log.state = 'Normal'
                # Move away from the goal
                if distance - pre_distance > 0:
                    ground_log.state = 'Error'
                    ground_log.stuck_err_logger(pre_distance, distance, distance - pre_distance)
                    print('Error')
                    error_mag = True
                    drive.turn_right()
                    time.sleep(5)
                    drive.stop()
                    pre_gps = gps
                    gps = GYSFDMAXB.read_GPSData()
                    pre_distance = distance
                    distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
                    data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
                    ground_log.state = 'Normal'
                    print('Finish Error Processing')
            if data[4] == 'Turn Right':
                drive.turn_right()
            elif data[4] == 'Turn Left':
                drive.turn_left()
            time.sleep(0.3)
            if error_mag:
                drive.forward()
                time.sleep(0.7)
            pre_gps = gps
            gps = GYSFDMAXB.read_GPSData()
            pre_distance = distance
            distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
            data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
            ground_log.ground_logger(data, distance)
        gps = GYSFDMAXB.read_GPSData()
        distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
        print("distance : ", distance)
        ground_log.ground_logger(data, distance)
        if distance <= 8: # Reach the goal within 8m
            print("Close to the goal")
            drive.stop()
            ground_log.end_of_ground_phase()
            break
        drive.forward()
        time.sleep(5)
        gps = GYSFDMAXB.read_GPSData()
        data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
        pre_distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
        ground_log.ground_logger(data, pre_distance)

    """
    Image Processing Phase
    """
    phase = 3
    print("phase : ", phase)
    drive.unfold_camera()
    img_proc_log = logger.ImgProcLogger()
    while phase == 3:
        img_name = img_proc.take_picture()
        cone_loc, proc_img_name, p = img_proc.detect_cone(img_name)
        gps = GYSFDMAXB.read_GPSData()
        distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
        print("distance :", distance)
        img_proc_log.img_proc_logger(img_name, proc_img_name, cone_loc, p, distance, gps)
        if p > 0.12:
            print("Reach the goal")
            img_proc_log.end_of_img_proc_phase()
            drive.forward()
            time.sleep(1.8)
            drive.stop()
            break
        if distance >= 15:
            print('Error')
            img_proc_log.err_logger(distance,gps)
            drive.stop()
            phase = 2
            break
        if cone_loc == "Front":
            drive.forward()
            if p < 0.001:
                time.sleep(1)
        elif cone_loc == "Right":
            drive.turn_right()
            time.sleep(0.4)
            if p < 0.001:
                time.sleep(0.3)
            drive.forward()
            if p < 0.001:
                time.sleep(1)
        elif cone_loc == "Left":
            drive.turn_left()
            time.sleep(0.4)
            if p < 0.001:
                time.sleep(0.3)
            drive.forward()
            if p < 0.001:
                time.sleep(1)
        else: # Not Found
            drive.forward()
            time.sleep(1)
        time.sleep(2)
        drive.stop()