from threading import Thread
from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
import time

# Empty list to store sequence of keypad presses
password = []
selected_option = None  # Variable to store the selected option

# Call back function invoked when any key on keypad is pressed
def key_pressed(key):
    global selected_option
    password.append(key)
    selected_option = key   # Update the selected option with the latest key press

    print(password)

def display_menu(lcd):
    lcd.clear()
    lcd.lcd_display_string("1. Collect Drink", 1)
    lcd.lcd_display_string("2. Purchase", 2)

def handle_user_selection(lcd):
    global selected_option
    while True:
        if selected_option == '1':
            lcd.clear()
            lcd.lcd_display_string("Face QR Code", 1)
            lcd.lcd_display_string("towards camera", 2)
        elif selected_option == '2':
            lcd.clear()
            lcd.lcd_display_string("1. Milo", 1)
            lcd.lcd_display_string("2. 100 Plus", 2)
        selected_option = None  # Reset selected option after handling

def main():
    # Initialise LCD
    lcd = LCD.lcd()
    lcd.clear()

    # Display something on LCD
    lcd.lcd_display_string("Welcome!", 1)
    time.sleep(2)   # Display for 2 seconds
    lcd.clear()

    # Initialise the HAL keypad driver
    keypad.init(key_pressed)

    # Display main menu
    display_menu(lcd)

    # Start a thread to handle user selection
    selection_thread = Thread(target=handle_user_selection, args=(lcd,))
    selection_thread.start()

    # Main thread can continue to do other things, or just wait for user selection to be handled
    selection_thread.join()

# Main entry potin
if __name__ == "__main__":
    main()