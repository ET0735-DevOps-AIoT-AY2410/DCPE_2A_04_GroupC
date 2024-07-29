from threading import Thread
from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
import time
import queue

lcd = LCD.lcd()
testValue = 0

# Empty list to store sequence of keypad presses
password = []
selected_option = None  # Variable to store the selected option

# Call back function invoked when any key on keypad is pressed
def key_pressed(key):
    global selected_option
    password.append(key)
    selected_option = key   # Update the selected option with the latest key press
    print(f"Key pressed: {key}")  # Debugging statement
    print(f"Updated selected_option: {selected_option}")  # Debugging statement

def display_menu(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("1. Collect Drink", 1, 0)
    lcd.lcd_display_string("2. Purchase", 2, 0)
    print("Menu displayed")  # Debugging statement

def handle_user_selection():
    global selected_option, testValue
    while True:
        if selected_option is not None:
            print(f"Handling selection: {selected_option}")  # Debugging statement
            if selected_option == '1':
                lcd.lcd_clear()
                lcd.lcd_display_string("Face QR Code", 1, 0)
                lcd.lcd_display_string("towards camera", 2, 0)
                testValue = 3
            elif selected_option == '2':
                lcd.lcd_clear()
                lcd.lcd_display_string("1. Milo", 1, 0)
                lcd.lcd_display_string("2. 100 Plus", 2, 0)
                testValue = 2
            selected_option = None  # Reset selected option after handling
        time.sleep(0.1)  # Small delay to prevent busy-waiting

def main_menu_flow():
    try:
        # Display main menu
        display_menu(lcd)

        # Initialise the HAL keypad driver
        keypad.init(key_pressed)

        # Start a thread to handle keypad input
        keypad_thread = Thread(target=keypad.get_key)
        keypad_thread.start()

        # Start a thread to handle user selection
        selection_thread = Thread(target=handle_user_selection)
        selection_thread.start()

        # Main thread can continue to do other things, or just wait for user selection to be handled
        selection_thread.join()
        keypad_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main_menu_flow()
