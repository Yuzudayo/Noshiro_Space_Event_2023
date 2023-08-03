import pigpio
import time

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html
PINS = [19, 26, 12, 16, 25, 8]
FINS = [16, 25]
RINS = [12, 8]
SERVO = 17

class Motor(object):
    def __init__(self):
        Motor.pi = pigpio.pi()
        for pin in PINS:
            Motor.pi.set_mode(pin, pigpio.OUTPUT)
            Motor.pi.set_PWM_frequency(pin, 10000)
            Motor.pi.set_PWM_range(pin, 100)
    
    def forward(self):
        [Motor.pi.set_PWM_dutycycle(pin, 100) for pin in FINS]
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in RINS]
        print("forward")
        
    def back(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in FINS]
        [Motor.pi.set_PWM_dutycycle(pin, 80) for pin in RINS]
        print("back")
    
    def stop(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in PINS]
        print("stop")
        
    def turn_right(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in RINS]
        Motor.pi.set_PWM_dutycycle(16, 100)
        Motor.pi.set_PWM_dutycycle(25, 50)
        print("turn right")
    
    def turn_left(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in RINS]
        Motor.pi.set_PWM_dutycycle(16, 50)
        Motor.pi.set_PWM_dutycycle(25, 100)
        print("turn left")
        
    def stuck(self):
        Motor.back(self)
        time.sleep(3)
        Motor.turn_right(self)
        time.sleep(1)
        Motor.forward(self)
        time.sleep(3)
        Motor.stop(self)
        print('Finish stuck processing')
        
    def set_angle(angle):
        # 角度を500から2500のパルス幅にマッピングする
        pulse_width = (angle / 180) * (2500 - 500) + 500
        
        # パルス幅を設定してサーボを回転させる
        Motor.pi.set_servo_pulsewidth(SERVO, pulse_width)
    
    def servo(self):
        # Motor.pi.set_servo_pulsewidth(SERVO, 2400)
        # time.sleep(1)
        # Motor.pi.set_servo_pulsewidth(SERVO, 1700)
        # time.sleep(1)
        # Motor.pi.set_servo_pulsewidth(SERVO, 500)
        # time.sleep(1)
        # Motor.pi.set_servo_pulsewidth(SERVO, 0)
        Motor.set_angle(160)
        print("Separation mechanism activated")
        
    def unfold_camera(self):
        Motor.pi.set_PWM_dutycycle(26, 0)
        Motor.pi.set_PWM_dutycycle(19, 60)
        time.sleep(20)
        Motor.stop(self)
        print("Unfold camera")
    
    def camera_motor(self):
        Motor.pi.set_PWM_dutycycle(26, 0)
        Motor.pi.set_PWM_dutycycle(19, 60)
        print("Camera motor activated")
        
    def camera_motor_reverse(self):
        Motor.pi.set_PWM_dutycycle(26, 60)
        Motor.pi.set_PWM_dutycycle(19, 0)
        print("Camera motor activated reverse")
        
    def attach_para(self):
        # Motor.pi.set_servo_pulsewidth(SERVO, 2400)
        # time.sleep(3)
        # Motor.pi.set_servo_pulsewidth(SERVO, 0)
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
            print('Wrong input')
