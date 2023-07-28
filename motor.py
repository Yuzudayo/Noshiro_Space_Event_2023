import pigpio
import time

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html
PINS = [6, 13, 19, 26, 20, 21]
FINS = [6, 19, 20]
RINS = [13, 26, 21]

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
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in FINS]
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in RINS]
        print("stop")
        
    def turn_right(self):
        
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in RINS]
        print("turn right")
    
    def turn_left(self):
        
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in RINS]
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
        
    def sepa_mecha(self):

        print("Separation mechanism activated")
        
    def attach_para(self):
        print("Parachute attached")
        

if __name__ == '__main__':
    drive = Motor()
    movement = {'w': drive.forward, 'a': drive.turn_left, 'd': drive.turn_right, 's': drive.back, 'q': drive.stop, 'st': drive.stuck, 'sep': drive.sepa_mecha, 'para': drive.attach_para}
    while True:
        c = input('Enter char : ')
        if c in movement.keys():
            movement[c]()
        else:
            print('Wrong input')
