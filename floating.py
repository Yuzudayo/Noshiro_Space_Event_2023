import bme280
import time
import logger
import motor

SEA_LEVEL_PRESSURE = 1013.25

def cal_altitude(init_altitude):
    bme280.read_BaroData() # discard the first value
    time.sleep(0.1)
    data = bme280.read_BaroData()
    """
    data[0] = pressure
    data[1] = temperature
    data[2] = altitude
    
    https://keisan.casio.jp/exec/system/1257609530
    altitude = (Sea level pressure / Current pressure)**(1 / 5.257) - 1) * (Current temperature + 273.15) / 0.0065
    """
    data[2] = ((SEA_LEVEL_PRESSURE / data[0])**(1 / 5.257) - 1) * (data[1] + 273.15) / 0.0065 - init_altitude
    return data

if __name__ == '__main__':
    floating_log = logger.FloatingLogger()
    drive = motor.Motor()
    state = 'Rising'
    floating_log.state = 'Rising'
    print("initial altitude")
    data = cal_altitude(0)
    init_altitude = data[2]
    floating_log.floating_logger(data)
    print("Rising phase")
    while state != 'Landing':
        """
        state Rising
              Ascent Completed
              Landing
              Error
        """
        while state == 'Rising':
            data = cal_altitude(init_altitude)
            altitude = data[2]
            floating_log.floating_logger(data)
            print("Rising")
            if altitude >= 5:
                state = 'Ascent Completed'
                floating_log.state = 'Ascent Completed'
            time.sleep(1)
        while state == 'Ascent Completed':
            data = cal_altitude(init_altitude)
            altitude = data[2]
            floating_log.floating_logger(data)
            print("Ascent Completed")
            if altitude <= 3:
                state = 'Landing'
                floating_log.state = 'Landing'
            time.sleep(0.1)
        floating_log.end_of_floating_phase()
        drive.servo() # Separation mechanism activated