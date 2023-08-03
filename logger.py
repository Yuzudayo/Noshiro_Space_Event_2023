import datetime
import csv

"""
phase 1 : Floating
      2 : Ground 
      3 : Image Processing
"""

class Floating_logger(object):
    filename = ''
    state = 0
    """
    state 1 : Rising
          2 : Falling
          3 : Landing
         -1 : Error
    """

    def __init__(self):
        now = datetime.datetime.now()
        Floating_logger.filename = 'floating/' + now.strftime('%Y%m%d_%H%M%S') + '_floating.csv'
        with open(Floating_logger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['state', '1:Rising', '2:Falling', '3:Landing', '-1:Error'])
            writer.writerow(['time', 'state', 'pressure', 'temperature', 'altitude'])
        f.close()
    
    def floating_logger(self, data):
        with open(Floating_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state] + data)
        f.close()
        
    def error_logger(self, altitude):
        with open(Floating_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state, 'altitude', altitude])
        f.close()
        
    def end_of_floating_phase(self):
        with open(Floating_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state, 'Separation mechanism activated'])
        f.close()
        
class Ground_logger(object):
    filename = ''
    state = 'None'
    """
    state Normal
          Stuck
          Error
    """
    
    def __init__(self):
        now = datetime.datetime.now()
        Ground_logger.filename = 'ground/' + now.strftime('%Y%m%d_%H%M%S') + '_ground.csv'
        with open(Ground_logger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'state', 'Distance to goal', 'To destination angle', 'Heading angle','Angle difference', 'Is heading goal', 'direction', 'longtitude', 'latitude', 'magX', 'magY', 'magZ', 'accelX', 'accelY', 'accelZ', 'calib status mag', 'calib status accel'])
            # calib status : 0 ~ 3
        f.close()
    
    def ground_logger(self, data, distance):
        with open(Ground_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), Ground_logger.state, distance] + data)
            
    def stuck_err_logger(self, distance, later_distance, diff_distance):
        with open(Ground_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), Ground_logger.state, 'distance', distance, 'distance after 5 seconds', later_distance, 'distance difference', diff_distance])

    def end_of_ground_phase(self):
        with open(Ground_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), Ground_logger.state, ' Start image processing'])
        f.close()
        
class Img_proc_logger(object):
    filename = ''
    """
    cone location Front
                  Right
                  Left
                  Not Found
    """
    def __init__(self):
        now = datetime.datetime.now()
        Img_proc_logger.filename = 'img_proc/' + now.strftime('%Y%m%d_%H%M%S') + '_img_proc.csv'
        with open(Img_proc_logger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'cone place', 'img name', 'processed img name', 'percentage of cone in img', 'Distance to goal', 'longtitude', 'latitude'])
        f.close()
        
    def img_proc_logger(self, img_name, proc_img_name, cone_loc, p, distance, gps):
        with open(Img_proc_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), cone_loc, img_name, proc_img_name, p, distance] + gps)
            
    def err_logger(self, distance, gps):
        with open(Img_proc_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), 'Error', 'distance', distance] + gps)
    
    def end_of_img_proc_phase(self):
        with open(Img_proc_logger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), 'Reach the goal'])
        f.close()