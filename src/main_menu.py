from threading import Thread
from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
import time
import queue

lcd = LCD.lcd()
lcd.lcd_clear()

testValue = 0
shared_keypad_queue = queue.Queue()
selected_option = None

def key_pressed(key):
    shared_keypad_queue.put()

def display_menu():
    lcd.lcd_clear()
    lcd.lcd_display_string("1. Collect Drink", 1, 0)
    lcd.lcd_display_string("2. Purchase", 2, 0)
    print("Menu displayed")

def handle_user_selection():
    global selected_option, testValue
    while True:
        if selected_option is not None:
            print(f"Handling selection: {selected_option}")
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
            selected_option = None
        time.sleep(0.1)

def main_menu_flow():
    display_menu()
        
    # Run monitor_keypad in the main thread
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    # Start a thread to handle user selection
    selection_thread = Thread(target=handle_user_selection)
    selection_thread.start()

    # Main thread can continue to do other things, or just wait for user selection to be handled
    selection_thread.join()
    keypad_thread.join()

if __name__ == "__main__":
    main_menu_flow()
