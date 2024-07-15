from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
import time

# Define the image and font paths
image_path = r'C:\Local_Git_Repository\CA\DCPE_2A_04_GroupC\test.jpg'
font_path = r'C:\Windows\Fonts\Arial.ttf'

def activate_camera():
    print("Activating camera")
    from picamera2 import Picamera2, Preview

    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(
        main={"size": (1920, 1080)},
        lores={"size": (640, 480)},
        display="lores"
    )
    
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file(image_path)  # Save the image to the defined path
    print("Camera activated and image captured")
    picam2.stop_preview()
    picam2.close()

def check_qr_code(data):
    return data == "valid_code"

def dispense_drink():
    print("Dispensing purchased drink")

def qr_code_detection():
    print('Face QR Code Towards Camera')

    try:
        # Open the captured image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Load the font
        font = ImageFont.truetype(font_path, size=20)

        # Decode any barcodes/QR codes in the image
        for d in decode(img):
            # Draw a rectangle around the detected barcode
            draw.rectangle(
                ((d.rect.left, d.rect.top), (d.rect.left + d.rect.width, d.rect.top + d.rect.height)),
                outline=(0, 0, 255), width=3
            )
            # Draw a polygon around the detected barcode
            draw.polygon(d.polygon, outline=(0, 255, 0), width=3)
            # Draw the decoded data as text
            draw.text(
                (d.rect.left, d.rect.top + d.rect.height), d.data.decode(),
                (255, 0, 0), font=font
            )

            # Print the decoded data
            data = d.data.decode()
            print("QR Code detected: ", data)
            if check_qr_code(data):
                dispense_drink()
                return
            else:
                print("Invalid QR Code. Please try again.")

        print("No QR code detected. Please face the QR code towards the camera.")
        img.show()
        
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    activate_camera()
    qr_code_detection()

if __name__ == '__main__':
    main()
