import time
from threading import Thread
import queue

from hal import hal_led as led
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from hal import hal_lcd as LCD

# Queue to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

lcd = LCD.lcd()
lcd.lcd_clear()

def key_pressed(key):
    shared_keypad_queue.put(key)

def ir_sensor_security(correct_sequence, entered_sequence):
    while True:
        ir_value = ir_sensor.get_ir_sensor_state()
        if not ir_value and entered_sequence != correct_sequence:
            buzzer.beep(1, 1, 3)  # Beep for 3 seconds continuously
        time.sleep(0.1)

def security():
    led.init()
    adc.init()
    buzzer.init()
    ir_sensor.init()
    servo.init()

    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    correct_sequence = [5, 6, 7]
    entered_sequence = []
    keyvalue = None

    # Start IR sensor monitoring in a separate thread
    ir_thread = Thread(target=ir_sensor_security, args=(correct_sequence, entered_sequence))
    ir_thread.start()

    while True:
        lcd.lcd_display_string("Door Closed", 1)
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            entered_sequence.append(keyvalue)

            if len(entered_sequence) > len(correct_sequence):
                entered_sequence.pop(0)

            if entered_sequence == correct_sequence:
                lcd.lcd_display_string("Authorization", 1, 0)
                lcd.lcd_display_string("Granted", 2, 0)
                buzzer.turn_off()
                servo.set_servo_position(90)
                entered_sequence.clear()
                time.sleep(2)
                lcd.lcd_clear()

                # Wait for '*' key to be pressed
                lcd.lcd_display_string("Press '*' to", 1, 0)
                lcd.lcd_display_string("continue", 2, 0)
                while True:
                    if not shared_keypad_queue.empty():
                        keyvalue = shared_keypad_queue.get()
                        print(f"Key pressed: {keyvalue}")  # Debug statement
                        if keyvalue == "*":
                            break  # Exit the loop if '*' is pressed

                # After '*' is pressed
                lcd.lcd_display_string("Continuing...", 1, 0)
                time.sleep(2)
                servo.set_servo_position(0)
                lcd.lcd_clear()

        print(keyvalue)  # Debug statement to print key values
        time.sleep(0.1)

if __name__ == "__main__":
    security()