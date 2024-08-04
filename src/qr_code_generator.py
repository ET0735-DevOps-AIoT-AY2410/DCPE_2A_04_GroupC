import qrcode
import random
import os

# Define the src directory path
src_dir = "src"
os.makedirs(src_dir, exist_ok=True)

def qr_generate():
    qr_code_data = random.randint(0, 100)
    print(f"Generated QR Data: {qr_code_data}")
    qr_img = qrcode.make(qr_code_data)
    qr_img_path = os.path.join(src_dir, "qr-img.jpg")
    qr_img.save(qr_img_path)
    print(f"Saved QR code image to {qr_img_path}")

def qr_generatepay():
    qr_code_data = random.randint(0, 100)
    print(f"Generated QR Data: {qr_code_data}")
    qr_img = qrcode.make(qr_code_data)
    qr_img_path = os.path.join(src_dir, "qr-pay.jpg")
    qr_img.save(qr_img_path)
    print(f"Saved QR code image to {qr_img_path}")

if __name__ == '__main__':
    qr_generate()
    qr_generatepay()


