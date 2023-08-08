import datetime
import csv

"""
phase 1 : Floating
      2 : Ground 
      3 : Image Processing
"""

class FloatingLogger(object):
    filename = ''
    state = 'None'
    """
    state Rising
          Ascent Completed
          Landing
    """

    def __init__(self):
        now = datetime.datetime.now()
        FloatingLogger.filename = 'floating/' + now.strftime('%Y%m%d_%H%M%S') + '_floating.csv'
        with open(FloatingLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'state', 'pressure', 'temperature', 'altitude', 'other description'])
        f.close()
    
    def floating_logger(self, data):
        with open(FloatingLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state] + data)
        f.close()
        
    def end_of_floating_phase(self, description='Separation mechanism activated'):
        with open(FloatingLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state, '', '', '', description])
        f.close()
        
class GroundLogger(object):
    filename = ''
    state = 'None'
    """
    state Normal
          Stuck
          Error
    """
    
    def __init__(self):
        now = datetime.datetime.now()
        GroundLogger.filename = 'ground/' + now.strftime('%Y%m%d_%H%M%S') + '_ground.csv'
        with open(GroundLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'state', 'Distance to goal', 'To destination angle', 'Heading angle','Angle difference', 'Is heading goal', 'direction', 'longtitude', 'latitude', 'magX', 'magY', 'magZ', 'accelX', 'accelY', 'accelZ', 'calib status mag', 'calib status accel'])
            # calib status : 0 ~ 3
        f.close()
    
    def ground_logger(self, data, distance):
        with open(GroundLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), GroundLogger.state, distance] + data)
            
    def stuck_err_logger(self, distance, later_distance, diff_distance):
        with open(GroundLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), GroundLogger.state, 'distance', distance, 'distance after 5 seconds', later_distance, 'distance difference', diff_distance])

    def end_of_ground_phase(self):
        with open(GroundLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), GroundLogger.state, ' Start image processing'])
        f.close()
        
class ImgProcLogger(object):
    filename = ''
    """
    cone location Front
                  Right
                  Left
                  Not Found
    """
    def __init__(self):
        now = datetime.datetime.now()
        ImgProcLogger.filename = 'img_proc/' + now.strftime('%Y%m%d_%H%M%S') + '_img_proc.csv'
        with open(ImgProcLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'cone place', 'img name', 'processed img name', 'percentage of cone in img', 'Distance to goal', 'longtitude', 'latitude'])
        f.close()
        
    def img_proc_logger(self, img_name, proc_img_name, cone_loc, p, distance, gps):
        with open(ImgProcLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), cone_loc, img_name, proc_img_name, p, distance] + gps)
            
    def err_logger(self, distance, gps):
        with open(ImgProcLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), 'Error', 'distance', distance] + gps)
    
    def end_of_img_proc_phase(self):
        with open(ImgProcLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), 'Reach the goal'])
        f.close()
        
class ErrorLogger(object):
    filename = ''
    """
    state Floating
          Ground
          Image Processing
    """
    def __init__(self):
        now = datetime.datetime.now()
        ErrorLogger.filename = 'error/' + now.strftime('%Y%m%d_%H%M%S') + '_error.csv'
        with open(ErrorLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'phase', 'error description', 'data'])
        f.close()
        
    def baro_error_logger(self, phase, data):
        with open(ErrorLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), phase, 'Altitude value decreases during ascent','pressure', data[0], 'temperature', data[1],'altitude', data[2]])
        f.close()
        