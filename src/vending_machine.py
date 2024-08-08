import time
from threading import Thread
import queue
import qr_code_generator
import camera_module
import cameradetect
import hogpayment

from picamera2 import Picamera2, Preview
from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_moisture_sensor as moisture_sensor
from hal import hal_input_switch as input_switch
from hal import hal_ir_sensor as ir_sensor
from hal import hal_rfid_reader as rfid_reader
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_usonic as usonic
from hal import hal_dc_motor as dc_motor
from hal import hal_accelerometer as accel

# Paths to the images
scan_image_path = r'/home/pi/ET0735/CA/src/scan.jpg'
pay_image_path = r'/home/pi/ET0735/CA/src/pay.jpg'
font_path = r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
collection_reference_image_path = r"/home/pi/ET0735/CA/src/qr-img.jpg"
payment_reference_image_path = r"/home/pi/ET0735/CA/src/qr-pay.jpg"


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
        qr_code_generator.qr_generate()
        camera_module.activate_camera()
        cameradetect.main()
        #(Go Back to Main Menu)

    elif keyvalue == 2:
        lcd.lcd_clear()
        lcd.lcd_display_string("1. Milo", 1, 0)
        lcd.lcd_display_string("2. 100 Plus", 2, 0)
        hogpayment.main()
        #(Go Back to Main Menu)

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
