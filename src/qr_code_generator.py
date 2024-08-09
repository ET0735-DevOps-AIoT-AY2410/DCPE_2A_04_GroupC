import qrcode
import random
<<<<<<< HEAD
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
=======
import qr_code_data
import os

def qr_generate():
    file_name = "qr-img.jpg"
    if os.path.exists(file_name):
        os.remove(file_name)
    qr_code_data.qr_data = random.randint(0, 100)
    print(f"Generated QR Data: {qr_code_data.qr_data}")
    qr_img = qrcode.make(qr_code_data.qr_data)
    qr_img.save(file_name)

def qr_generatepay():
    file_name = "qr-pay.jpg"
    if os.path.exists(file_name):
        os.remove(file_name)
    qr_code_data.qr_data = random.randint(0, 100)
    print(f"Generated QR Data: {qr_code_data.qr_data}")
    qr_img = qrcode.make(qr_code_data.qr_data)
    qr_img.save(file_name)
>>>>>>> ervin

if __name__ == '__main__':
    qr_generate()
    qr_generatepay()
