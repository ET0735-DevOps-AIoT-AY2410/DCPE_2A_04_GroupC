import time
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
from picamera2 import Picamera2, Preview
from hal import hal_lcd as LCD
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo

# Paths to the images
scan_image_path = r'/home/pi/ET0735/CA/src/scan.jpg'
pay_image_path = r'/home/pi/ET0735/CA/src/pay.jpg'
font_path = r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
collection_reference_image_path = r"/home/pi/ET0735/CA/src/qr-img.jpg"
payment_reference_image_path = r"/home/pi/ET0735/CA/src/qr-pay.jpg"

lcd = LCD.lcd()

def extract_qr_code_data(image_path):
    try:
        print(f"Attempting to open image at: {image_path}")
        img = Image.open(image_path)
        print(f"Image opened successfully. Size: {img.size}")
        decoded_objects = decode(img)
        if decoded_objects:
            print(f"QR code detected in {image_path}")
            return decoded_objects[0].data.decode()
        else:
            print(f"No QR code detected in reference image: {image_path}")
            return None
    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error extracting QR code data from {image_path}: {e}")
        return None

def activate_camera(image_path):
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(
        main={"size": (1920, 1080)},
        lores={"size": (640, 480)},
        display="lores"
    )

    try:
        picam2.configure(camera_config)
        picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(2)
        picam2.capture_file(image_path)
        picam2.stop_preview()
        picam2.close()
        print(f"Image captured successfully at {image_path}")
    except Exception as e:
        print(f"Failed to capture image: {e}")
        picam2.close()

def dispense_drink():
    print("Starting DC motor...")
    dc_motor.init()
    dc_motor.set_motor_speed(50)  # Set motor speed to 50%
    time.sleep(5)  # Run motor for 5 seconds
    dc_motor.set_motor_speed(0)

    print("Dispensing purchased drink with servo...")
    servo.init()
    servo.set_servo_position(0)  # Move servo to 0 degrees
    time.sleep(2)  # Wait for 2 seconds
    servo.set_servo_position(180)  # Move servo to 180 degrees
    time.sleep(2)  # Wait for 2 seconds

def qr_code_detection(scan_image_path, font_path, reference_codes):
    try:
        img = Image.open(scan_image_path)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(font_path, size=20)
        except IOError:
            print(f"Error: Cannot open font resource at {font_path}.")
            font = ImageFont.load_default()  # Fallback to default font

        decoded_objects = decode(img)
        if not decoded_objects:
            print("No QR code detected.")
            img.show()
            return False

        for d in decoded_objects:
            print(f"Decoded Data: {d.data.decode()}")
            print(f"Bounding Box: {d.rect}")
            draw.rectangle(
                ((d.rect.left, d.rect.top), (d.rect.left + d.rect.width, d.rect.top + d.rect.height)),
                outline=(0, 0, 255)
            )
            draw.polygon(d.polygon, outline=(0, 255, 0))
            draw.text(
                (d.rect.left, d.rect.top + d.rect.height), d.data.decode(),
                (255, 0, 0), font=font
            )

            data = d.data.decode()
            if data in reference_codes:
                print(f"Valid QR Code Detected: {data}")
                return True
            else:
                print(f"Invalid QR Code Detected: {data}")

        print("No valid QR code detected. Please try again.")
        img.show()
        return False
        
    except OSError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def pay_dispense(pay_image_path, font_path, reference_codes):
    activate_camera(pay_image_path)
    if qr_code_detection(pay_image_path, font_path, reference_codes):
        lcd.lcd_clear()
        lcd.lcd_display_string("Dispensing drink...", 1)
        print("Valid QR code detected. Dispensing drink...")
        dispense_drink()
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("Invalid QR code", 1)
        print("Invalid QR code. Please try again.")

def main():
    print("Starting main function")
    lcd.lcd_clear()
    lcd.lcd_display_string("Initializing...", 1)

    collection_reference_code = extract_qr_code_data(collection_reference_image_path)
    print(f"Collection reference code: {collection_reference_code}")
    payment_reference_code = extract_qr_code_data(payment_reference_image_path)
    print(f"Payment reference code: {payment_reference_code}")

    if collection_reference_code and payment_reference_code:
        reference_codes = [collection_reference_code, payment_reference_code]
        
        while True:
            lcd.lcd_clear()
            lcd.lcd_display_string("Camera Activated", 1)
            activate_camera(scan_image_path)
            if qr_code_detection(scan_image_path, font_path, reference_codes):
                lcd.lcd_clear()
                lcd.lcd_display_string("Dispensing drink...", 1)
                print("Valid QR code detected. Proceeding to dispense...")
                pay_dispense(pay_image_path, font_path, reference_codes)
                break
            else:
                lcd.lcd_clear()
                lcd.lcd_display_string("Invalid QR Code", 1)
                print("Invalid QR code. Please try again.")
                time.sleep(2)  # Wait for 2 seconds before trying again
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("QR Extraction Failed", 1)
        print("Unable to extract QR code data from reference images.")

if __name__ == '__main__':
    main()
