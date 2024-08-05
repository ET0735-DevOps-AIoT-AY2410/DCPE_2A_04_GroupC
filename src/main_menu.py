from threading import Thread
import time
import queue

# Initialize shared queue for keypad input
shared_keypad_queue = queue.Queue()

# Function to display the main menu on the LCD
def display_menu(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("1. Collect Drink", 1, 0)
    lcd.lcd_display_string("2. Purchase", 2, 0)

# Function to handle user selection based on keypad input
def handle_user_selection(lcd):
    keyvalue = shared_keypad_queue.get()
    print(f"Key value: {keyvalue}")

    if keyvalue == 1:
        lcd.lcd_clear()
        lcd.lcd_display_string("Face QR Code", 1, 0)
        lcd.lcd_display_string("towards camera", 2, 0)
    elif keyvalue == 2:
        lcd.lcd_clear()
        lcd.lcd_display_string("1. Milo", 1, 0)
        lcd.lcd_display_string("2. 100 Plus", 2, 0)

    time.sleep(10)  # Delay for readability

def main_menu_flow(lcd, keypad):

    # Initialize the HAL keypad driver
    keypad.init(shared_keypad_queue.put)

    # Start a thread to handle keypad input
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    while True:
        # Handle user selection in the main thread
        display_menu(lcd)
        handle_user_selection(lcd)
        time.sleep(0.5)

if __name__ == "__main__":
    from hal import hal_keypad as keypad
    from hal import hal_lcd as LCD

    # Initialize LCD
    lcd = LCD.lcd()
    lcd.lcd_clear()

    main_menu_flow(lcd, keypad)
