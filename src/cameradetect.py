import time
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo
from time import sleep

# Paths to the images
payment_reference_image_path = r"/home/pi/ET0735/CA/src/qr-pay.jpg"
collection_reference_image_path = r"/home/pi/ET0735/CA/src/qr-img.jpg"
scan_image_path = r'/home/pi/ET0735/CA/src/scan.jpg'
pay_image_path = r'/home/pi/ET0735/CA/src/qr-pay.jpg'
# Path to the font
font_path = r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def extract_qr_code_data(image_path):
    try:
        img = Image.open(image_path)
        decoded_objects = decode(img)
        if decoded_objects:
            return decoded_objects[0].data.decode()  # Assuming the image contains one QR code
        else:
            print("No QR code detected in reference image.")
            return None
    except Exception as e:
        print(f"Error extracting QR code data: {e}")
        return None

def activate_camera(image_path):
    from picamera2 import Picamera2, Preview

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
    sleep(5)  # Run motor for 5 seconds
    dc_motor.set_motor_speed(0)

    print("Dispensing purchased drink with servo...")
    servo.init()
    servo.set_servo_position(0)  # Move servo to 0 degrees
    sleep(2)  # Wait for 2 seconds
    servo.set_servo_position(180)  # Move servo to 180 degrees
    sleep(2)  # Wait for 2 seconds

def qr_code_detection(scan_image_path, font_path, reference_code):
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
            if data == reference_code:
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

def main():
    collection_reference_code = extract_qr_code_data(collection_reference_image_path)
    if collection_reference_code:
        activate_camera(scan_image_path)
        if qr_code_detection(scan_image_path, font_path, collection_reference_code):
            print("Collection QR code valid. Ready for the next step.")
            pay_dispense(pay_image_path, font_path, collection_reference_code)
        else:
            print("Collection QR code invalid. Please try again.")
    else:
        print("Unable to extract QR code data from collection reference image.")

def pay_dispense(pay_image_path, font_path, payment_reference_code):
    activate_camera(pay_image_path)
    if qr_code_detection(pay_image_path, font_path, payment_reference_code):
        print("Payment QR code valid. Dispensing drink...")
        dispense_drink()
    else:
        print("Payment QR code invalid. Please try again.")

if __name__ == '__main__':
    main()
