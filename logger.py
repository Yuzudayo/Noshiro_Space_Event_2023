import datetime
import csv

"""
phase 1 : Floating
      2 : Ground 
      3 : Image Processing
      4 : Reach the goal
"""

class FloatingLogger(object):
    filename = ''
    state = 'None'
    """
    state Rising
          Ascent Completed
          Landing
          Error
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
          Something Wrong
    """
    
    def __init__(self):
        now = datetime.datetime.now()
        GroundLogger.filename = 'ground/' + now.strftime('%Y%m%d_%H%M%S') + '_ground.csv'
        with open(GroundLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            # calib status : 0 ~ 3
            writer.writerow(['time', 'state', 'distance to goal', 'destination angle', 'heading angle','angle difference', 'heading goal', 'direction', 'longtitude', 'latitude', 'magX', 'magY', 'magZ', 'accelX', 'accelY', 'accelZ', 'calib status mag', 'calib status accel', 'pre longtitude', 'pre latitude', 'error geomagnetic sensor', 'error heading flags','description'])
        f.close()
    
    def ground_logger(self, data, distance, error_mag=False, error_heading=0, pre_gps=[0,0], description=''):
        with open(GroundLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state, distance] + data + pre_gps + [error_mag, error_heading, description])

    def end_of_ground_phase(self, discription='Start Image Processing'):
        with open(GroundLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '','', discription])
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
            writer.writerow(['time', 'cone place', 'img name', 'processed img name', 'percentage of cone in img', 'Distance to goal', 'longtitude', 'latitude', 'pre longtitude', 'pre latitude', 'discription'])
        f.close()
        
    def img_proc_logger(self, img_name, proc_img_name, cone_loc, p, distance, gps, pre_gps=[0,0], description=''):
        with open(ImgProcLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), cone_loc, img_name, proc_img_name, p, distance] + gps + pre_gps + [description])
        f.close()    
    
    def end_of_img_proc_phase(self):
        with open(ImgProcLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), '', '', '', '', '', '', '', '', '', 'Reach the goal'])
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
        
    def geomag_error_logger(self, phase, data):
        with open(ErrorLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), phase, 'The accuracy of the geomagnetic sensor is not good','destination angle', data[0], 'heading angle', data[1],'angle difference', data[2], 'magX', data[6][0], 'magY', data[6][1], 'magZ', data[6][2], 'calib status mag', data[6][6]])
        f.close()
        
    def heading_error_logger(self, phase, pre_gps, gps, pre_distance, distance, error_mag=False, error_heading=0):
        with open(ErrorLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), phase, 'previous longtitude', pre_gps[0], 'previous latitude', pre_gps[1], 'longtitude', gps[0], 'latitude', gps[1], 'previous distance', pre_distance, 'distance', distance, 'error geomagnetic sensor', error_mag, 'error heading flags', error_heading, 'The heading direction is not correct'])
        f.close()
        
    def gps_error_logger(self, phase, pre_gps, gps, pre_distance, distance, error_mag=False, error_heading=0):
        with open(ErrorLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), phase, 'previous longtitude', pre_gps[0], 'previous latitude', pre_gps[1], 'longtitude', gps[0], 'latitude', gps[1], 'previous distance', pre_distance, 'distance', distance, 'error geomagnetic sensor', error_mag, 'error heading flags', error_heading, 'Poor GPS accuracy'])
        f.close()
        
    def far_error_logger(self, phase, gps, distance, error_heading=0):
        with open(ErrorLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), phase, 'longtitude', gps[0], 'latitude', gps[1], 'distance', distance, 'error heading flags', error_heading,'The rover is far from the goal'])
        f.close()
        
    def img_proc_error_logger(self, phase, error_mag=False, error_heading=0, distance=0):
        with open(ErrorLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), phase, 'error geomagnetic sensor', error_mag, 'error heading flags', error_heading, 'distance', distance, 'Image processing failed'])
        f.close()
        