# import floating
import bno055
import datetime
import csv
import time

def drop_test():
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d_%H%M%S') + '_floating.csv'
    while True:
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            data = bno055.read_Mag_AccelData()
            writer.writerow([data[0], data[1], data[2], data[3][0], data[3][1], data[3][2], data[4]])
            print(data)
        f.close()
        time.sleep(0.01)
        
        
        
  
  
if __name__ == "__main__":
    drop_test()