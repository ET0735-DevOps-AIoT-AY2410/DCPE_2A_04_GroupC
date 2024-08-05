import time
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo
from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_rfid_reader as rfid_reader
from time import sleep
import cameradetect
from picamera2 import Picamera2, Preview

# Paths to the images
collection_reference_image_path = r"/home/pi/ET0735/CA/src/qr-img.jpg"
payment_reference_image_path = r"/home/pi/ET0735/CA/src/qr-pay.jpg"
scan_image_path = r'/home/pi/ET0735/CA/src/scan.jpg'
pay_image_path = r'/home/pi/ET0735/CA/src/pay.jpg'
font_path = r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

APPROVED_IDS = ["977573770339", "711535355173","910820273072"]

def is_payment_successful(card_id):
    return card_id in APPROVED_IDS



def user_selects_drink():
    print("Select drink:\n1. Milo\n2. 100 Plus")
    drink = input("Enter your choice (1 or 2): ")
    return drink

def user_selects_payment_method():
    print("Select payment method:\n1. Card\n2. App")
    method = input("Enter your choice (1 or 2): ")
    return method

def main():
    print("Starting main function")
    
    # Initialize hardware
    lcd = LCD.lcd()
    led.init()
    lcd.backlight(1)
    lcd.lcd_clear()
    reader = rfid_reader.init()

    collection_reference_code = cameradetect.extract_qr_code_data(collection_reference_image_path)
    print(f"Collection reference code: {collection_reference_code}")
    payment_reference_code = cameradetect.extract_qr_code_data(payment_reference_image_path)
    print(f"Payment reference code: {payment_reference_code}")
    
    if collection_reference_code and payment_reference_code:
        reference_codes = [collection_reference_code, payment_reference_code]
        
        while True:
            drink = user_selects_drink()

            if drink not in ["1", "2"]:
                print("Invalid selection. Restarting...")
                continue
            
            payment_method = user_selects_payment_method()
            
            if payment_method == "2":  # App
                cameradetect.pay_dispense(pay_image_path, font_path, reference_codes)
                
            elif payment_method == "1":  # Card
                lcd.lcd_display_string("Tap RFID card", 1) 

                while True:
                    id = reader.read_id_no_block()
                    id = str(id)
                    
                    if id != "None":
                        print("RFID card ID = " + id)
                        
                        # Display RFID card ID on LCD line 2
                        lcd.lcd_display_string(id, 2)
                        time.sleep(3)
                        lcd.lcd_display_string("Checking Payment",1)
                        time.sleep(3)
                        
                        # Check if payment is successful
                        if is_payment_successful(id):
                            print("Payment successful.")
                            lcd.lcd_display_string("Payment Success", 1)
                            led.set_output(0, 1)  # Turn on LED to indicate success
                            cameradetect.dispense_drink()
                            time.sleep(5)  # Keep the message for 5 seconds
                            break
                        else:
                            print("Payment failed.")
                            lcd.lcd_display_string("Payment Failed", 1)
                            led.set_output(0, 0)  # Ensure LED is off
                            time.sleep(5)  # Keep the message for 5 seconds
                        
                        # Clear the LCD for the next read
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Tap RFID card", 1)
                        break  # Exit the while loop and restart the process

            else:
                print("Invalid payment method. Restarting...")
                continue

    else:
        print("Unable to extract QR code data from reference images.")

if __name__ == "__main__":
    main()
