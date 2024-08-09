import time
from threading import Thread,Event
import queue
import qr_code_generator
import hogpayment
from detect_door_open import security
from force_detect import monitor_accelerometer
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad

# Initialize shared queue for keypad input
shared_keypad_queue = queue.Queue()

# Event to signal when the LCD should be on or off
lcd_on_event = Event()

# Dictionary to store the current display state
current_display_state = {
    "line1": "",
    "line2": ""
}

# Function to update the display state
def update_display_state(line1, line2):
    current_display_state["line1"] = line1
    current_display_state["line2"] = line2

# Function to display the main menu on the LCD
def display_menu(lcd):
    lcd.lcd_clear()
    line1 = "1. Collect Drink"
    line2 = "2. Purchase"
    lcd.lcd_display_string(line1, 1, 0)
    lcd.lcd_display_string(line2, 2, 0)
    update_display_state(line1, line2)

# Function to handle user selection based on keypad input
def handle_user_selection(lcd):
    while True:
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            print(f"Key value: {keyvalue}")

            # Reset the timer event whenever a key is pressed
            lcd_on_event.set()

            if keyvalue == 1:
                lcd.lcd_clear()
                line1 = "Face QR Code"
                line2 = "towards camera"
                lcd.lcd_display_string(line1, 1, 0)
                lcd.lcd_display_string(line2, 2, 0)
                update_display_state(line1, line2)
                qr_code_generator.qr_generate()
                time.sleep(5)  # Wait for 5 seconds
                break  # Return to main menu

            elif keyvalue == 2:
                lcd.lcd_clear()
                line1 = "1. Milo"
                line2 = "2. 100 Plus"
                lcd.lcd_display_string(line1, 1, 0)
                lcd.lcd_display_string(line2, 2, 0)
                update_display_state(line1, line2)
                time.sleep(2)  # Buffer time for user to select drink

                # Check for drink selection
                if not shared_keypad_queue.empty():
                    keyvalue = shared_keypad_queue.get()
                    print(f"Drink Option Key value: {keyvalue}")

                    if keyvalue == 1:
                        lcd.lcd_clear()
                        line1 = "Milo Selected"
                        line2 = ""
                        lcd.lcd_display_string(line1, 1, 0)
                        update_display_state(line1, line2)
                        qr_code_generator.qr_generatepay()
                        hogpayment.main()
                        time.sleep(2)
                    elif keyvalue == 2:
                        lcd.lcd_clear()
                        line1 = "100 Plus"
                        line2 = "Selected"
                        lcd.lcd_display_string(line1, 1, 0)
                        lcd.lcd_display_string(line2, 2, 0)
                        update_display_state(line1, line2)
                        qr_code_generator.qr_generatepay()
                        hogpayment.main()
                        time.sleep(2)
                break  # Return to main menu

        time.sleep(0.1)  # Small delay to prevent CPU overutilization

    # Ensure that the menu is re-displayed after a user selection
    display_menu(lcd)
    lcd_on_event.set()  # Keep the LCD on after menu is redisplayed

# Function to manage the power state of the LCD
def power_manage(lcd):
    while True:
        # Wait for the event to be set, indicating activity
        if lcd_on_event.wait(timeout=20):
            # If the event was set, reset it and continue the loop
            lcd_on_event.clear()
        else:
            # If the event was not set within 20 secs, turn off the LCD
            lcd.lcd_clear()
            lcd.backlight(0)  # Turn off the LCD backlight
            print("LCD powered off due to inactivity.")  # Debug statement

            # Wait until a key press is detected again
            while shared_keypad_queue.empty():
                time.sleep(0.05)

            print("Key pressed, waking up LCD.")  # Debug statement
            lcd.backlight(1)  # Turn the LCD backlight on

            # Restore the previous display state
            lcd.lcd_display_string(current_display_state["line1"], 1, 0)
            lcd.lcd_display_string(current_display_state["line2"], 2, 0)

            lcd_on_event.set()  # Turn the LCD back on

def main_menu_flow(lcd, keypad):
    # Initialize the HAL keypad driver
    keypad.init(shared_keypad_queue.put)

    # Start a thread to handle power management
    power_thread = Thread(target=power_manage, args=(lcd,))
    power_thread.start()

    # Start a thread to handle keypad input
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    while True:
        # Set the LCD on event to ensure the display is on initially
        lcd_on_event.set()

        # Display the main menu and wait for user selection
        display_menu(lcd)
        handle_user_selection(lcd)

        # Pause the loop if the LCD is off
        while not lcd_on_event.is_set():
            time.sleep(0.1)

        time.sleep(0.2)

if __name__ == "__main__":
    from hal import hal_keypad as keypad
    from hal import hal_lcd as LCD

    # Initialize LCD
    lcd = LCD.lcd()
    lcd.lcd_clear()

    # Start the security system in a separate thread
    security_thread = Thread(target=security)
    security_thread.start()

    accel_thread = Thread(target=monitor_accelerometer)
    accel_thread.start()

    main_menu_flow(lcd, keypad)
