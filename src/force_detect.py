from hal import hal_accelerometer as acc
from hal import hal_buzzer as buzz

buzz.init()
acc.init()
acc.ADXL345().calibrate()

def monitor_accelerometer(acc):
    while True:
        x, y, z = acc.get_3_axis()
        total_g = (x**2 + y**2 + z**2)**0.5
        if total_g > 20:    # 20g threshold
            buzz.turn_on_with_timer(200)
