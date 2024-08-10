import time
from threading import Thread, Event
import queue
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad

# Shared queue for keypad input
shared_keypad_queue = queue.Queue()

# Event to signal when the LCD should be on or off
lcd_on_event = Event()

# Event to track LCD power mode
lcd_low_power_mode_event = Event()

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

            lcd_on_event.set()

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
                        time.sleep(2)
                    elif keyvalue == 2:
                        lcd.lcd_clear()
                        line1 = "100 Plus"
                        line2 = "Selected"
                        lcd.lcd_display_string(line1, 1, 0)
                        lcd.lcd_display_string(line2, 2, 0)
                        update_display_state(line1, line2)
                        time.sleep(2)
                return  # Exit to loop back to main menu

            elif keyvalue == "#":
                # Enter password entry mode
                lcd.lcd_clear()
                line1 = "Enter password:"
                lcd.lcd_display_string(line1, 1, 0)
                update_display_state(line1, "")
                time.sleep(2)
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

def main_menu_flow(lcd, keypad):
    keypad.init(shared_keypad_queue.put)

    power_thread = Thread(target=power_manage, args=(lcd,))
    power_thread.start()

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    while True:
        lcd_on_event.set()
        display_menu(lcd)
        handle_user_selection(lcd)  # Call handle_user_selection which will return to main menu

        time.sleep(0.2)

if __name__ == "__main__":
    lcd = LCD.lcd()
    lcd.lcd_clear()

    main_menu_flow(lcd, keypad)
