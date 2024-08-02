from threading import Thread
from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
import time
import queue

# Initialize LCD
lcd = LCD.lcd()
lcd.lcd_clear()

# Create a shared queue for keypad input
shared_keypad_queue = queue.Queue()

# Callback function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

# Function to display the main menu on the LCD
def display_menu():
    lcd.lcd_clear()
    lcd.lcd_display_string("1. Collect Drink", 1, 0)
    lcd.lcd_display_string("2. Purchase", 2, 0)

# Function to handle user selection based on keypad input
def handle_user_selection():
    keyvalue = shared_keypad_queue.get()
    print(f"Key value: {keyvalue}")

    if (keyvalue == 1):
        lcd.lcd_clear()
        lcd.lcd_display_string("Face QR Code", 1, 0)
        lcd.lcd_display_string("towards camera", 2, 0)
    elif (keyvalue == 2):
        lcd.lcd_clear()
        lcd.lcd_display_string("1. Milo", 1, 0)
        lcd.lcd_display_string("2. 100 Plus", 2, 0)
        
    time.sleep(2)  # Delay for readability

def main_menu_flow():

    # Initialize the HAL keypad driver
    keypad.init(key_pressed)

    # Start a thread to handle keypad input
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    while True:
        # Handle user selection in the main thread
        display_menu()
        handle_user_selection()
        time.sleep(1)

if __name__ == "__main__":
    main_menu_flow()
