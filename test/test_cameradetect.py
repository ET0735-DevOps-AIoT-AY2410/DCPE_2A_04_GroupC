from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
import qrcode
import os

# Define paths
src_dir = os.path.join(os.getcwd(), "src")
images_dir = os.path.join(src_dir, "images")
qr_image_path = os.path.join(images_dir, "qr-code.jpg")

def qr_generate(image_path):
    qr_code_data = "1234"  # Fixed QR code data for testing
    qr_img = qrcode.make(qr_code_data)
    qr_img.save(image_path)
    print(f"QR code image saved to {image_path}")

def qr_code_detection(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"Image path does not exist: {image_path}")
            return False
        
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        # Use default font
        font = ImageFont.load_default()

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
                outline='blue'
            )
            draw.polygon(d.polygon, outline='green')
            draw.text(
                (d.rect.left, d.rect.top + d.rect.height), d.data.decode(),
                fill='red', font=font
            )

            if d.data.decode() == "1234":
                print(f"Valid QR Code Detected: {d.data.decode()}")
                img.show()
                return True

        print("No valid QR code detected.")
        img.show()
        return False
        
    except OSError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == '__main__':
    # Ensure the images directory exists
    os.makedirs(images_dir, exist_ok=True)

    qr_generate(qr_image_path)
    qr_code_detection(qr_image_path)
