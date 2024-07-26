import time
from threading import Thread
from hal import hal_accelerometer as acc
from hal import hal_buzzer as buzz

buzz.init()
acc.init()
acc.ADXL345().calibrate()

def start(self):
    # Start monitoring the accelerometer in a seperate thread
    acc_thread = Thread(target=monitor_accelerometer, args=acc)
    acc_thread.start()

    acc_thread.join()
    
def monitor_accelerometer(acc):
    while True:
        x, y, z = acc.get_3_axis()
        total_g = (x**2 + y**2 + z**2)**0.5
        if total_g > 20:    # 20g threshold
            buzz.beep(200, 200, 3)

        time.sleep(0.1) # reduce the number of checks
