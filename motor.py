import pigpio
import time
import numpy as np

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html
FRONT = [16, 26] # Left, Right
REAR = [12, 19] # Left, Right
CAM_FIN = 20
CAM_RIN = 21
PINS = FRONT + REAR + [CAM_FIN, CAM_RIN]
SERVO = 17

class Motor(object):
    def __init__(self):
        Motor.pi = pigpio.pi()
        for pin in PINS:
            Motor.pi.set_mode(pin, pigpio.OUTPUT)
            Motor.pi.set_PWM_frequency(pin, 10000)
            Motor.pi.set_PWM_range(pin, 100)
    
    def forward(self):
        [Motor.pi.set_PWM_dutycycle(pin, 100) for pin in FRONT]
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("forward")
        
    def back(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in FRONT]
        [Motor.pi.set_PWM_dutycycle(pin, 100) for pin in REAR]
        print("back")
    
    def stop(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in PINS]
        print("stop")
        
    def turn_right(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], 70) # Left
        Motor.pi.set_PWM_dutycycle(FRONT[1], 100) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn right")
        
    def back_right(self):
        Motor.pi.set_PWM_dutycycle(REAR[0], 0) # Left
        Motor.pi.set_PWM_dutycycle(REAR[1], 100) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in FRONT]
    
    def turn_left(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], 100) # Left
        Motor.pi.set_PWM_dutycycle(FRONT[1], 70) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn left")
        
    def back_left(self):
        Motor.pi.set_PWM_dutycycle(REAR[0], 100) # Left
        Motor.pi.set_PWM_dutycycle(REAR[1], 0) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in FRONT]
        
    def stuck(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], 100) # Left
        Motor.pi.set_PWM_dutycycle(REAR[0], 0)
        Motor.pi.set_PWM_dutycycle(FRONT[1], 0) # Right
        Motor.pi.set_PWM_dutycycle(REAR[1], 100)
        time.sleep(3.7)
        Motor.stop(self)
        print('Finish stuck processing')
        
    def set_angle(angle):
        # Mapping angles to pulse widths from 500 to 2500
        pulse_width = (angle / 180) * (2500 - 500) + 500
        # Set the pulse width and rotate the servo
        Motor.pi.set_servo_pulsewidth(SERVO, pulse_width)
    
    def servo(self):
        Motor.set_angle(160)
        print("Separation mechanism activated")
        
    def unfold_camera(self):
        Motor.pi.set_PWM_dutycycle(CAM_FIN, 0)
        Motor.pi.set_PWM_dutycycle(CAM_RIN, 90)
        time.sleep(15)
        Motor.stop(self)
        print("Unfold camera")
    
    def camera_motor(self):
        Motor.pi.set_PWM_dutycycle(CAM_FIN, 0)
        Motor.pi.set_PWM_dutycycle(CAM_RIN, 90)
        print("Camera motor activated")
        
    def camera_motor_reverse(self):
        Motor.pi.set_PWM_dutycycle(CAM_FIN, 90)
        Motor.pi.set_PWM_dutycycle(CAM_RIN, 0)
        print("Camera motor activated reverse")
        
    def attach_para(self):
        Motor.set_angle(0)
        print("Parachute attached")
        

if __name__ == '__main__':
    drive = Motor()
    movement = {'w': drive.forward, 'a': drive.turn_left, 'd': drive.turn_right, 's': drive.back, 'q': drive.stop, 'st': drive.stuck, 'sep': drive.servo, 'cam': drive.unfold_camera, 'para': drive.attach_para, 'camr': drive.camera_motor_reverse, 'camf': drive.camera_motor}
    while True:
        c = input('Enter char : ')
        if c in movement.keys():
            movement[c]()
        elif c == 'z':
            break
        else:
            print('Invalid input')
