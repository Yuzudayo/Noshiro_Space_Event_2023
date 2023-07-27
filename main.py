"""
    NOSHIRO SPACE EVENT 2023
    ASTRUM MAIN PROGRAM
    
    Author : Yuzu
    Language : Python Ver.3.9.2
    Last Update : 07/27/2023
"""

import GYSFDMAXB
import motor
import ground
import floating
import img_proc
import logger
import time

print("Initializing")
GYSFDMAXB.read_GPSData()
ground.cal_heading_angle()
floating.cal_altitude()
time.sleep(1)
drive = motor.Motor()

print("start!!")

"""
Floating Phase
"""
phase = 1
print("phase : ", phase)
floating_log = logger.Floating_logger()
"""
state 1 : Rising
      2 : Falling
      3 : Landing
     -1 : Error
"""
state = 1
floating_log.state = 1
start = time.time()
data = floating.cal_altitude()
init_altitude = data[2]
print("initial altitude : {}." .format(init_altitude()))
floating_log.floating_logger(data)
print("Rising phase")
while phase == 1:
    while state == 1:
        data = floating.cal_altitude()
        altitude = data[2]
        floating_log.floating_logger(data)
        print("Rising")
        # Incorrect sensor value
        if altitude < init_altitude - 5:
            state = -1
            floating_log.state = -1
            floating_log.error_logger(altitude)
            print("Error")
        if altitude >= init_altitude + 8:
            state = 2
            floating_log.state = 2
        now = time.time()
        if now - start > 900:
            print('5 minutes passed')
            state = 3
            floating_log.state = 3
            break
        print("altitude : {}." .format(altitude))
        time.sleep(1.5)
    while state == 2:
        data = floating.cal_altitude()
        altitude = data[2]
        floating_log.floating_logger(data)
        print("Falling")
        if altitude <= init_altitude + 3:
            state = 3
            floating_log.state = 3
        now = time.time()
        if now - start > 900:
            print('5 minutes passed')
            state = 3
            floating_log.state = 3
            break
        print("altitude : {}." .format(altitude))
        time.sleep(0.2)
    while state == -1:
        now = time.time()
        if now - start > 900:
            print('5 minutes passed')
            state = 3
            floating_log.state = 3
            break
        time.sleep(1)
    print("Landing")
    time.sleep(5)
    floating_log.end_of_floating_phase()
    drive.sepa_mecha() # Separation mechanism activated
    time.sleep(12)
    break

reach_the_goal = False
while not reach_the_goal:
    """
    Ground Phase
    """
    phase = 2
    print("phase : ", phase)
    ground_log = logger.Ground_logger()
    logger.Ground_logger.state = 'Normal'
    while phase == 2:
        distance = ground.cal_distance(ground.des_lng, ground.des_lat)
        print("distance : ", distance)
        data = ground.is_heading_goal()
        ground_log.ground_logger(data, distance)
        if distance <= 6: # Reach the goal within 6m
            print("Close to the goal")
            drive.stop()
            ground_log.end_of_ground_phase()
            break
        while data[3] != True: # Not heading the goal
            if data[4] == 'Turn Right':
                drive.turn_right()
            elif data[4] == 'Turn Left':
                drive.turn_left()
            time.sleep(0.3)
            data = ground.is_heading_goal()
            ground_log.ground_logger(data, distance)
        drive.forward()
        time.sleep(5)
        later_distance = ground.cal_distance(ground.des_lng, ground.des_lat)
        # Stuck Processing
        if abs(distance - later_distance) < 0.1 and distance != later_distance:
            logger.Ground_logger.state = 'Stuck'
            ground_log.stuck_err_logger(distance, later_distance, abs(distance - later_distance))
            print('stuck')
            drive.stuck()
            logger.Ground_logger.state = 'Normal'
        # Move away from the goal
        if later_distance - distance > 0.5:
            logger.Ground_logger.state = 'Error'
            ground_log.stuck_err_logger(distance, later_distance, distance - later_distance)
            print('Error')
            drive.turn_right()
            time.sleep(5)
            logger.Ground_logger.state = 'Normal'
            print('Finish Error Processing')

    """
    Image Processing Phase
    """
    phase = 3
    print("phase : ", phase)
    img_proc_log = logger.Img_proc_logger()
    while phase == 3:
        img_name = img_proc.take_a_picture()
        cone_loc, proc_img_name, p = img_proc.detect_cone(img_name)
        distance = ground.cal_distance(ground.des_lng, ground.des_lat)
        print("distance :", distance)
        data = ground.is_heading_goal()
        gps = [data[5], data[6]]
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
            drive.turn_right()
            time.sleep(5)
            drive.stop()
            continue
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