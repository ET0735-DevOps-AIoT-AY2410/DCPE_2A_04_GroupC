from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
import time
from qr_code_generator import qr_data, qr_generate

# Define the image and font paths
image_path = r'/mnt/data/test.jpg'  # Update to match your actual path if necessary
font_path = r'/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'

def activate_camera():
    print("Activating camera")
    #from picamera2 import Picamera2, Preview

    #picam2 = Picamera2()
    #camera_config = picam2.create_still_configuration(
        #main={"size": (1920, 1080)},
        #lores={"size": (640, 480)},
        #display="lores"
    #)
    
    #picam2.configure(camera_config)
    #picam2.start_preview(Preview.QTGL)
    #picam2.start()
    time.sleep(2)
    #picam2.capture_file(image_path)  # Save the image to the defined path
    #print("Camera activated and image captured")
    #picam2.stop_preview()
    #picam2.close()

def check_qr_code(data):
    print(f"Checking QR Code: {data} against generated QR Code: {qr_data}")
    return data == str(qr_data)

def dispense_drink():
    print("Dispensing purchased drink")

def qr_code_detection():
    print('Face QR Code Towards Camera')

    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype(font_path, size=20)
        except IOError:
            print("Font not found. Using default font.")
            font = ImageFont.load_default()

        for d in decode(img):
            draw.rectangle(
                ((d.rect.left, d.rect.top), (d.rect.left + d.rect.width, d.rect.top + d.rect.height)),
                outline=(0, 0, 255), width=3
            )
            draw.polygon(d.polygon, outline=(0, 255, 0))
            draw.text(
                (d.rect.left, d.rect.top + d.rect.height), d.data.decode(),
                (255, 0, 0), font=font
            )

            data = d.data.decode()
            print(f"QR Code detected: {data}")
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
    qr_generate()  # Generate the QR code before activating the camera
    activate_camera()
    qr_code_detection()

if __name__ == '__main__':
    main()

