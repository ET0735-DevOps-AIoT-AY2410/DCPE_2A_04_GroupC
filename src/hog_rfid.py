from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_rfid_reader as rfid_reader
import time 

APPROVED_IDS = ["977573770339", "711535355173","910820273072"]

def is_payment_successful(card_id):
    return card_id in APPROVED_IDS



def main():
    # Get lcd instance
    lcd = LCD.lcd()

    # Initialize LED HAL driver
    led.init()

    lcd.backlight(1)
    lcd.lcd_clear()

    # Display message on LCD
    lcd.lcd_display_string("Tap RFID card", 1) 

    # Turn off LED initially
    led.set_output(0, 0)

    # Initialize RFID card reader
    reader = rfid_reader.init()

    # Infinite loop to scan for RFID cards
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
                time.sleep(5)  # Keep the message for 5 seconds
            else:
                print("Payment failed.")
                lcd.lcd_display_string("Payment Failed", 1)
                led.set_output(0, 0)  # Ensure LED is off
                time.sleep(5)  # Keep the message for 5 seconds
            
            # Clear the LCD for the next read
            lcd.lcd_clear()
            lcd.lcd_display_string("Tap RFID card", 1)

# Main entry point
if __name__ == "__main__":
    main()