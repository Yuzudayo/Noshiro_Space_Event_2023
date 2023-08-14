"""""""""""""""""""""""""""""""""""
    NOSHIRO SPACE EVENT 2023
    ASTRUM MAIN FALLBACK PROGRAM
    
    Author : Yuzu
    Language : Python Ver.3.9.2
    Last Update : 08/12/2023
"""""""""""""""""""""""""""""""""""


import GYSFDMAXB
import motor
import ground
import img_proc
import logger
import time
import datetime
import csv

# destination point(lon, lat)
DESTINATION = [139.65490166666666, 35.950921666666666]


with open('sys_error.csv', 'a') as f:
                    now = datetime.datetime.now()
                    writer = csv.writer(f)
                    writer.writerow([now.strftime('%H:%M:%S'), 'Launch fallback program'])
                    f.close()
print("Hello World!!")
error_log = logger.ErrorLogger()
drive = motor.Motor()
drive.stop()
drive.servo() # Separation mechanism activated

"""
phase (1 : Floating)
      2 : Ground 
      3 : Image Processing
      4 : Reach the goal
"""


reach_goal = False
# The flag that identifies abnormalities in the geomagnetic sensor
error_mag = False
# The counter that detects sensor anomalies from the heading direction 
error_heading = 0
# The flag that identifies abnormalities in the image processing
error_img_proc = False
# Variable used for stack determination and GPS direction determination
pre_gps = [0,0]
phase = 2
# The flag indicating if the camera is deployed
unfold_camera = False
ground_log = logger.GroundLogger()
ground_log.state = 'Normal'
img_proc_log = logger.ImgProcLogger()

while not reach_goal:
    """
    Ground Phase
    """
    print("phase : ", phase)
    while GYSFDMAXB.read_GPSData() == [0,0]:
            print("Waiting for GPS reception")
            time.sleep(5)
    gps = GYSFDMAXB.read_GPSData()
    data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
    distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
    ground_log.ground_logger(data, distance, error_mag, error_heading)
    while phase == 2 and error_heading < 5:
        count = 0 # Counter for geomagnetic sensor abnormalities
        while data[3] != True: # Not heading the goal
            count += 1
            # Abnormal geomagnetic sensor
            if count >= 20:
                error_mag = True
                ground_log.state = 'Something Wrong'
                error_log.geomag_error_logger(phase, data)
                break
            # Check the stack and position when there are many position adjustments
            if count % 10 == 0:
                stuck, diff_distance = ground.is_stuck(pre_gps, gps)
                # Stuck Processing
                if stuck:
                    ground_log.state = 'Stuck'
                    ground_log.ground_logger(data, distance, error_mag, error_heading, pre_gps, 'Stuck judgment because the movement distance is {}m'.format(diff_distance))
                    print('stuck')
                    drive.stuck()
                    pre_gps = gps
                    gps = GYSFDMAXB.read_GPSData()
                    pre_distance = distance
                    distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
                    data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
                    ground_log.state = 'Normal' if error_mag == False else 'Something Wrong'
                # Move away from the goal
                elif distance - pre_distance > 0.1:
                    ground_log.state = 'Something Wrong'
                    error_heading += 1
                    error_log.heading_error_logger(phase, pre_gps, gps, pre_distance, distance, error_mag, error_heading)
                    print('Error : Heading direction is wrong')
                    drive.turn_right()
                    time.sleep(5)
                    drive.stop()
                    pre_gps = gps
                    gps = GYSFDMAXB.read_GPSData()
                    distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
                    data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
                    ground_log.state = 'Normal'
                    print('Finish Error Processing')
            if data[4] == 'Turn Right':
                drive.turn_right()
            elif data[4] == 'Turn Left':
                drive.turn_left()
            time.sleep(0.3)
            if error_mag: # When controlling only with GPS, set the period to 1 second
                drive.forward()
                time.sleep(0.7)
            # The Value used for direction calculation with only position information
            pre_gps = gps
            gps = GYSFDMAXB.read_GPSData()
            # The value used to check if the rover is heading towards the goal
            pre_distance = distance
            distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
            data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
            ground_log.ground_logger(data, distance, error_mag, error_heading, pre_gps)
        if distance <= 8 and error_img_proc == False: # Reach the goal within 8m
            print("Close to the goal")
            drive.stop()
            ground_log.end_of_ground_phase()
            phase = 3
            break
        if distance <= 1 and error_img_proc: # Reach the goal within 1m
            print("Reach the goal")
            phase = 4
            ground_log.end_of_ground_phase('Reach the goal without image processing')
            drive.forward()
            time.sleep(1.8)
            drive.stop()
            break
        drive.forward()
        time.sleep(5)
        pre_gps = gps
        gps = GYSFDMAXB.read_GPSData()
        data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
        pre_distance = distance
        distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
        ground_log.ground_logger(data, distance, error_mag, error_heading, pre_gps)
        # Check the stack and position
        stuck, diff_distance = ground.is_stuck(pre_gps, gps)
        # Stuck Processing
        if stuck:
            ground_log.state = 'Stuck'
            ground_log.ground_logger(data, distance, error_mag, pre_gps, 'Stuck judgment because the movement distance is {}m'.format(diff_distance))
            print('Stuck')
            drive.stuck()
            pre_gps = gps
            gps = GYSFDMAXB.read_GPSData()
            pre_distance = distance
            distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
            data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
            ground_log.state = 'Normal' if error_mag == False else 'Something Wrong'
        # Move away from the goal
        elif distance - pre_distance > 0.1:
            ground_log.state = 'Something Wrong'
            error_heading += 1
            error_log.heading_error_logger(phase, pre_gps, gps, pre_distance, distance, error_mag, error_heading)
            print('Error : Heading direction is wrong')
            drive.turn_right()
            time.sleep(5)
            drive.stop()
            pre_gps = gps
            gps = GYSFDMAXB.read_GPSData()
            distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
            data = ground.is_heading_goal(gps, DESTINATION, pre_gps, error_mag)
            ground_log.state = 'Normal' if error_mag == False else 'Something Wrong'
            print('Finish Error Processing')
        if error_heading >= 5 and error_img_proc == False:
            ground_log.state = 'Something Wrong'
            print('Error : Poor GPS accuracy')
            error_log.gps_error_logger(phase, pre_gps, gps, pre_distance, distance, error_mag, error_heading)
            drive.stop()
            phase = 3
            
            
    """
    Image Processing Phase
    """
    print("phase : ", phase)
    if unfold_camera == False:
        drive.unfold_camera()
        unfold_camera = True
    while phase == 3 and error_img_proc == False:
        img_name = img_proc.take_picture()
        if img_name is not None:
            try:
                cone_loc, proc_img_name, p = img_proc.detect_cone(img_name)
            except Exception as e:
                print("Error : Image processing failed")
                error_img_proc = True
                img_proc_log.img_proc_error_logger(phase, error_mag, error_heading, distance=0)
                with open('sys_error.csv', 'a') as f:
                    now = datetime.datetime.now()
                    writer = csv.writer(f)
                    writer.writerow([now.strftime('%H:%M:%S'), 'Image processing failed', str(e)])
                    f.close()
                drive.stop()
                break
        else:
            error_img_proc = True
            img_proc_log.img_proc_error_logger(phase, error_mag, error_heading, distance=0)
            drive.stop()
            break
        pre_gps = gps if gps is not None else [0,0]
        gps = GYSFDMAXB.read_GPSData()
        distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
        print("distance :", distance)
        img_proc_log.img_proc_logger(img_name, proc_img_name, cone_loc, p, distance, gps, pre_gps)
        stuck, diff_distance = ground.is_stuck(pre_gps, gps)
        # Stuck Processing
        if stuck:
            img_proc_log.img_proc_logger(img_name, proc_img_name, cone_loc, p, distance, gps, pre_gps, 'Stuck judgment because the movement distance is {}m'.format(diff_distance))
            print('stuck')
            drive.stuck()
            pre_gps = gps
            gps = GYSFDMAXB.read_GPSData()
            distance = ground.cal_distance(gps[0], gps[1], DESTINATION[0], DESTINATION[1])
            continue
        if p > 0.12:
            print("Reach the goal")
            phase = 4
            img_proc_log.end_of_img_proc_phase()
            drive.forward()
            time.sleep(1.8)
            drive.stop()
            break
        if distance >= 15:
            print('Error : The rover is far from the goal')
            error_log.far_error_logger(phase, gps, distance, error_heading)
            drive.stop()
            if error_heading < 5:
                phase = 2
                break
            else:
                drive.turn_right()
                time.sleep(5)
                drive.stop()
        if cone_loc == "Front":
            drive.forward()
        elif cone_loc == "Right":
            drive.turn_right()
            time.sleep(0.5)
            drive.forward()
        elif cone_loc == "Left":
            drive.turn_left()
            time.sleep(0.5)
            drive.forward()
        else: # Not Found
            drive.turn_right()
        time.sleep(3) if p < 0.001 else time.sleep(2)
        drive.stop()