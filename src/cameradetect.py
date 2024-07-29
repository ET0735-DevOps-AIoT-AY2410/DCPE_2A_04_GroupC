import time
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode

# Paths to the images
reference_image_path = r"/home/pi/ET0735/CA/src/qr-img.jpg"
scan_image_path = r'C:\Local_Git_Repository\CA\DCPE_2A_04_GroupC\scan.jpg'
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
    print("Dispensing purchased drink")

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
                dispense_drink()
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
    reference_code = extract_qr_code_data(reference_image_path)
    if reference_code:
        activate_camera(scan_image_path)
        qr_code_detection(scan_image_path, font_path, reference_code)
    else:
        print("Unable to extract QR code data from reference image.")

if __name__ == '__main__':
    main()
