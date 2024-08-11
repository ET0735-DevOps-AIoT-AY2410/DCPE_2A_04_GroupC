import time
import queue
from threading import Thread, Event
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_led as led
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from hal import hal_accelerometer as acc
from hal import hal_dc_motor as dc_motor
from hal import hal_rfid_reader as rfid_reader

APPROVED_IDS = ["977573770339", "711535355173","910820273072"]

def is_payment_successful(card_id):
    return card_id in APPROVED_IDS

# Shared queue for keypad input
shared_keypad_queue = queue.Queue()

# Event to signal when the LCD should be on or off
lcd_on_event = Event()

# Event to track LCD power mode
lcd_low_power_mode_event = Event()

# Global variable to control buzzer state
buzzer_active = True

# Dictionary to store the current display state
current_display_state = {
    "line1": "",
    "line2": ""
}

def update_display_state(line1, line2):
    current_display_state["line1"] = line1
    current_display_state["line2"] = line2

def display_menu(lcd):
    lcd.lcd_clear()
    line1 = "1. Collect Drink"
    line2 = "2. Purchase"
    lcd.lcd_display_string(line1, 1, 0)
    lcd.lcd_display_string(line2, 2, 0)
    update_display_state(line1, line2)

def handle_user_selection(lcd):
    while True:
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            print(f"Key value: {keyvalue}")

            if lcd_low_power_mode_event.is_set():
                # Do nothing if the LCD is in low power mode
                print("LCD is in low power mode. Ignoring key press.")
                continue

            lcd_on_event.set()  # Ensure LCD stays on

            if keyvalue == 1:
                lcd.lcd_clear()
                line1 = "Face QR Code"
                line2 = "towards camera"
                lcd.lcd_display_string(line1, 1, 0)
                lcd.lcd_display_string(line2, 2, 0)
                update_display_state(line1, line2)
                time.sleep(5)  # Wait for 5 seconds
                return  # Exit to loop back to main menu

            elif keyvalue == 2:
                lcd.lcd_clear()
                line1 = "1. Milo"
                line2 = "2. 100 Plus"
                lcd.lcd_display_string(line1, 1, 0)
                lcd.lcd_display_string(line2, 2, 0)
                update_display_state(line1, line2)
                time.sleep(2)  # Buffer time for user to select drink

                if not shared_keypad_queue.empty():
                    keyvalue = shared_keypad_queue.get()
                    print(f"Drink Option Key value: {keyvalue}")

                    if keyvalue == 1:
                        lcd.lcd_clear()
                        line1 = "Milo Selected"
                        line2 = ""
                        lcd.lcd_display_string(line1, 1, 0)
                        update_display_state(line1, line2)
                        time.sleep(3)
                        hog_main()
                    elif keyvalue == 2:
                        lcd.lcd_clear()
                        line1 = "100 Plus"
                        line2 = "Selected"
                        lcd.lcd_display_string(line1, 1, 0)
                        lcd.lcd_display_string(line2, 2, 0)
                        update_display_state(line1, line2)
                        time.sleep(3)
                        hog_main()
                lcd.lcd_clear()
                return  # Exit to loop back to main menu

            elif keyvalue == "#":
                # Enter password entry mode and activate security
                lcd.lcd_clear()
                activate_security(lcd)
                return  # Exit to loop back to main menu

        time.sleep(0.1)

def power_manage(lcd):
    while True:
        if lcd_on_event.wait(timeout=20):
            lcd_on_event.clear()
            lcd_low_power_mode_event.clear()
        else:
            lcd.lcd_clear()
            lcd.backlight(0)
            print("LCD powered off due to inactivity.")
            lcd_low_power_mode_event.set()  # Set flag to indicate low power mode

            while shared_keypad_queue.empty():
                time.sleep(0.02)

            # Check if any key was pressed to wake up the LCD
            if not shared_keypad_queue.empty():
                lcd.lcd_clear()
                lcd.backlight(1)
                print("Key pressed, waking up LCD.")
                lcd.lcd_display_string(current_display_state["line1"], 1, 0)
                lcd.lcd_display_string(current_display_state["line2"], 2, 0)
                lcd_on_event.set()
                lcd_low_power_mode_event.clear()  # Clear the flag since LCD is now active

def ir_sensor_security(correct_sequence, entered_sequence):
    global buzzer_active
    while True:
        ir_value = ir_sensor.get_ir_sensor_state()

        # Check if IR sensor detects a signal and if the buzzer should be active
        if not ir_value and entered_sequence != correct_sequence and buzzer_active:
            buzzer.beep(1, 1, 3)  # Beep for 3 seconds continuously

        time.sleep(0.1)

def activate_security(lcd):
    global keyvalue, buzzer_active
    correct_sequence = [5, 6, 7]
    entered_sequence = []
    keyvalue = None

    while True:
        # Initial prompt display
        lcd.lcd_display_string("Enter password:", 1, 0)
        lcd_on_event.set()
        lcd_low_power_mode_event.clear()

        # Process keypad input
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            lcd_on_event.set()  # Keep LCD on with keypress
            entered_sequence.append(keyvalue)

            # Check if sequence is complete
            if len(entered_sequence) == len(correct_sequence):
                if entered_sequence == correct_sequence:
                    # Correct password entered
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Authorization", 1, 0)
                    lcd.lcd_display_string("Granted", 2, 0)
                    buzzer.turn_off()
                    buzzer_active = False # Update buzzer state flag
                    servo.set_servo_position(90)
                    time.sleep(2)
                    lcd.lcd_clear()

                    # Wait for '*' key to continue
                    lcd.lcd_display_string("Press '*' to", 1, 0)
                    lcd.lcd_display_string("continue", 2, 0)
                    while True:
                        if not shared_keypad_queue.empty():
                            keyvalue = shared_keypad_queue.get()
                            print(f"Key pressed: {keyvalue}")  # Debug statement
                            lcd_on_event.set()
                            if keyvalue == "*":
                                lcd_on_event.set()
                                break  # Exit loop when '*' is pressed

                    # Continue and reset the state
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Continuing...", 1, 0)
                    time.sleep(2)
                    servo.set_servo_position(0)
                    lcd.lcd_clear()
                    buzzer_active = True    # Restore buzzer state
                    return
                else:
                    # Incorrect password entered
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Wrong password", 1)
                    entered_sequence.clear()  # Clear the sequence
                    time.sleep(1)
                    lcd.lcd_clear()

        # Debug statement for key value
        print(f"Last key value: {keyvalue}")
        time.sleep(0.1)

def hog_main():
    print("Starting main function")

    lcd.lcd_clear()
    lcd.lcd_display_string("Tap RFID card", 1) 

    while True:
        lcd_on_event.set()
        id = reader.read_id_no_block()
        id = str(id)
                    
        if id != "None":
            print("RFID card ID = " + id)
                        
            # Display RFID card ID on LCD line 2
            lcd.lcd_clear()
            lcd.lcd_display_string(id, 2)
            time.sleep(3)
            lcd.lcd_display_string("Checking Payment",1)
            time.sleep(3)
                        
            # Check if payment is successful
            if is_payment_successful(id):
                print("Payment successful.")
                lcd.lcd_clear()
                lcd.lcd_display_string("Payment Success", 1)
                led.set_output(0, 1)  # Turn on LED to indicate success
                time.sleep(5)  # Keep the message for 5 seconds
                break
            else:
                print("Payment failed.")
                lcd.lcd_clear()
                lcd.lcd_display_string("Payment Failed", 1)
                led.set_output(0, 0)  # Ensure LED is off
                time.sleep(5)  # Keep the message for 5 seconds

        else:
            print("Invalid payment method. Restarting...")
            continue

def monitor_accelerometer(simulated_data=None):
    accelerometer = acc.init()

    while True:
        if simulated_data is not None:
            x, y, z = simulated_data  # Use simulated data if provided
        else:
            x, y, z = accelerometer.get_3_axis()

        total_g = (x*2 + y*2 + z*2)*0.5

        if total_g > 2:  # 2g threshold
            print("Vending machine shaken")
            buzzer.beep(1, 1, 3)

        time.sleep(0.2)  # Reduce the number of checks

def main_menu_flow(lcd, keypad):
    keypad.init(shared_keypad_queue.put)

    # Start background threads
    power_thread = Thread(target=power_manage, args=(lcd,))
    power_thread.start()

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    # Start IR sensor monitoring in a separate thread
    ir_thread = Thread(target=ir_sensor_security, args=([5, 6, 7], []))
    ir_thread.start()

    # Start accelerometer monitoring in a separate thread
    acc_thread = Thread(target=monitor_accelerometer)
    acc_thread.start()

    while True:
        lcd_on_event.set()
        display_menu(lcd)
        handle_user_selection(lcd)  # Call handle_user_selection which will return to main menu

        time.sleep(0.2)

if __name__ == "__main__":
    # Initialize all hardware components
    lcd = LCD.lcd()
    lcd.lcd_clear()
    reader = rfid_reader.init()
    led.init()
    adc.init()
    buzzer.init()
    ir_sensor.init()
    servo.init()
    acc.init()
    
    main_menu_flow(lcd, keypad)