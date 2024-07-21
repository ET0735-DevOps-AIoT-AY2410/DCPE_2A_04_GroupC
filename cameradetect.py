import time
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode

# Define the image and font paths
image_path = r'C:\Local_Git_Repository\CA\DCPE_2A_04_GroupC\test.jpg'
font_path = r'C:\Windows\Fonts\Arial.ttf'

def activate_camera(image_path):
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
    picam2.capture_file(image_path)
    picam2.stop_preview()
    picam2.close()

def check_qr_code(data):
    return data == "valid_code"

def dispense_drink():
    print("Dispensing purchased drink")

def qr_code_detection(image_path, font_path):
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, size=20)

        for d in decode(img):
            draw.rectangle(
                ((d.rect.left, d.rect.top), (d.rect.left + d.rect.width, d.rect.top + d.rect.height)),
                outline=(0, 0, 255), width=3
            )
            draw.polygon(d.polygon, outline=(0, 255, 0), width=3)
            draw.text(
                (d.rect.left, d.rect.top + d.rect.height), d.data.decode(),
                (255, 0, 0), font=font
            )

            data = d.data.decode()
            if check_qr_code(data):
                dispense_drink()
                return True
            else:
                print("Invalid QR Code. Please try again.")
                return False

        print("No QR code detected. Please face the QR code towards the camera.")
        img.show()
        return False
        
    except OSError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def main():
    activate_camera(image_path)
    qr_code_detection(image_path, font_path)

if __name__ == '__main__':
    main()
