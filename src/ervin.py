import time
from threading import Thread
import queue

from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_moisture_sensor as moisture_sensor
from hal import hal_input_switch as input_switch
from hal import hal_ir_sensor as ir_sensor
from hal import hal_rfid_reader as rfid_reader
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_usonic as usonic
from hal import hal_dc_motor as dc_motor
from hal import hal_accelerometer as accel

#Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

def key_pressed(key):
    shared_keypad_queue.put(key)

def security():
    led.init()
    adc.init()
    buzzer.init()
    moisture_sensor.init()
    input_switch.init()
    ir_sensor.init()
    reader = rfid_reader.init()
    servo.init()
    temp_humid_sensor.init()
    usonic.init()
    dc_motor.init()
    accelerometer = accel.init()

    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    lcd = LCD.lcd()
    lcd.lcd_clear()

    keyvalue = shared_keypad_queue.get()
    ir_value = ir_sensor.get_ir_sensor_state()
    if(keyvalue == 5): 
        if (keyvalue == 6):
            if (keyvalue == 7):
                lcd.lcd_display_string("Authorization", 1)
                lcd.lcd_display_string("Granted", 2)
                time.sleep(2)
                ir_sensor.turn_off()
                time.sleep(2)
                buzzer.turn_off()
                servo.set_servo_position(90)

                if (keyvalue == "*"):
                    ir_sensor.turn_on()
                    time.sleep(2)
                    buzzer.turn_on()
                    servo.set_servo_position(90)
    
        return keyvalue

    if (ir_value == False):
        buzzer.beep(0.5, 0.5, 1)
        return ir_value

def main():
    security()    

if __name__ == "__main__":
    main()  


    