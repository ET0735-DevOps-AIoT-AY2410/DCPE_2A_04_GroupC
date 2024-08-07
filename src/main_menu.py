from threading import Thread, Event
import time
import queue

# Initialize shared queue for keypad input
shared_keypad_queue = queue.Queue()

# Event to signal when the LCD should be on or off
lcd_on_event = Event()

# Function to display the main menu on the LCD
def display_menu(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("1. Collect Drink", 1, 0)
    lcd.lcd_display_string("2. Purchase", 2, 0)

# Function to handle user selection based on keypad input
def handle_user_selection(lcd):
    keyvalue = shared_keypad_queue.get()
    print(f"Key value: {keyvalue}")

    # Reset the timer event whenever a key is pressed
    lcd_on_event.set()

    if keyvalue == 1:
        lcd.lcd_clear()
        lcd.lcd_display_string("Face QR Code", 1, 0)
        lcd.lcd_display_string("towards camera", 2, 0)
    elif keyvalue == 2:
        lcd.lcd_clear()
        lcd.lcd_display_string("1. Milo", 1, 0)
        lcd.lcd_display_string("2. 100 Plus", 2, 0)

    time.sleep(5)  # Delay for readability

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
        # Set the LCD on event to ensure the dusplay is on initially
        lcd_on_event.set()

        # Handle user selection in the main thread
        display_menu(lcd)
        handle_user_selection(lcd)
        time.sleep(0.5)

def power_manage(lcd):
    while True:
        # Wait for the event to be set, indicating activity
        if lcd_on_event.wait(timeout=30):
            # If the event was set, reset it and continue the loop
            lcd_on_event.clear()
        else:
            # If the event was not set within 30 secs, turn off the LCD
            lcd.lcd_clear()
            print("LCD powered off due to inactivity.") # Debug statement
            lcd_on_event.clear()    # Clear the event flag

            # Wait until a key press is detected again
            shared_keypad_queue.get()
            lcd_on_event.set()  # Turn the LCD back on

if __name__ == "__main__":
    from hal import hal_keypad as keypad
    from hal import hal_lcd as LCD

    # Initialize LCD
    lcd = LCD.lcd()
    lcd.lcd_clear()

    main_menu_flow(lcd, keypad)
