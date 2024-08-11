import qrcode
import random
import os

# Directory to save text files inside the src folder
src_dir = os.path.join(os.getcwd(), "src")

# Directory to save QR images outside the src folder
images_dir = os.path.join(os.getcwd(), "images")

# Ensure the src and images directories exist
os.makedirs(src_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

# File paths for text files (in the src directory)
qr_data_file = os.path.join(src_dir, "qr_data.txt")
pay_data_file = os.path.join(src_dir, "pay_data.txt")

def save_qr_data(data, filename):
    with open(filename, "w") as file:
        file.write(str(data))

def qr_generate():
    qr_code_data = random.randint(0, 100)
    save_qr_data(qr_code_data, qr_data_file)
    print(f"Generated QR Data: {qr_code_data}")
    qr_img = qrcode.make(qr_code_data)
    qr_img_path = os.path.join(images_dir, "qr-img.jpg")
    qr_img.save(qr_img_path)
    print(f"Saved QR code image to {qr_img_path}")

def qr_generatepay():
    pay_data = random.randint(0, 100)
    save_qr_data(pay_data, pay_data_file)
    print(f"Generated Payment QR Data: {pay_data}")
    qr_img = qrcode.make(pay_data)
    qr_img_path = os.path.join(images_dir, "qr-pay.jpg")
    qr_img.save(qr_img_path)
    print(f"Saved payment QR code image to {qr_img_path}")

if __name__ == '__main__':
    qr_generate()
    qr_generatepay()