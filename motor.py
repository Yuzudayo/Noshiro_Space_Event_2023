import pigpio
import time

DEVICE_ADDRESS = 0x20
REG_IODIRA = 0x00 # GPA I/O direction register
REG_IODIRB = 0x01 # GPB I/O direction register
REG_OLATA = 0x14 # GPA output latch register
REG_OLATB = 0x15 # GPB output latch register

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html

class Motor(object):
    def __init__(self):
        Motor.pi = pigpio.pi()
        Motor.pi.set_mode(4, pigpio.OUTPUT)
        Motor.pi.set_mode(4, pigpio.OUTPUT)
        Motor.pi.set_mode(4, pigpio.OUTPUT)
        Motor.pi.set_mode(4, pigpio.OUTPUT)
        Motor.pi.set_mode(4, pigpio.OUTPUT)
        Motor.pi.set_mode(4, pigpio.OUTPUT)
    
    def forward(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x30)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x06)
        print("forward")
        
    def back(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x06)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x30)
        print("back")
    
    def stop(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x00)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x00)
        print("stop")
        
    def turn_right(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x36)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x00)
        print("turn right")
    
    def turn_left(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x00)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x36)
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
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x00)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x08)
        print("Separation mechanism activated")
        
    def attach_para(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x08)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x00)
        

if __name__ == '__main__':
    drive = Motor()
    movement = {'w': drive.forward, 'a': drive.turn_left, 'd': drive.turn_right, 's': drive.back, 'q': drive.stop, 'st': drive.stuck, 'sep': drive.sepa_mecha, 'para': drive.attach_para}
    while True:
        c = input('Enter char : ')
        if c in movement.keys():
            movement[c]()
        else:
            print('Wrong input')
