import time
from threading import Thread

def start():
    # Start monitoring the accelerometer in a separate thread
    acc_thread = Thread(target=monitor_accelerometer)
    acc_thread.start()

def monitor_accelerometer(simulated_data=None):
    # Initialization of HAL modules
    buzz.init()
    accelerometer = acc.init()

    while True:
        if simulated_data is not None:
            x, y, z = simulated_data  # Use simulated data if provided
        else:
            x, y, z = accelerometer.get_3_axis()

        total_g = (x**2 + y**2 + z**2)**0.5
        print(total_g)  # Debug statement

        if total_g > 2.5:  # 2.5g threshold
            buzz.beep(1, 1, 3)

        time.sleep(0.2)  # Reduce the number of checks

if __name__ == "__main__":
    from hal import hal_accelerometer as acc
    from hal import hal_buzzer as buzz
    
    monitor_accelerometer()
