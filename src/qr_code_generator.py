import qrcode
import random
import os

# Directory paths
raspberry_pi_images_dir = r'/home/pi/ET0735/CA/src/images'
local_images_dir = os.path.join(os.getcwd(), "src", "images")

# Ensure the directories exist
os.makedirs(raspberry_pi_images_dir, exist_ok=True)
os.makedirs(local_images_dir, exist_ok=True)

# File paths for text files
src_dir = os.path.join(os.getcwd(), "src")
qr_data_file = os.path.join(src_dir, "qr_data.txt")
pay_data_file = os.path.join(src_dir, "pay_data.txt")

def save_qr_data(data, filename):
    with open(filename, "w") as file:
        file.write(str(data))

def save_qr_image(qr_img, filename):
    qr_img.save(filename)
    print(f"Saved QR code image to {filename}")

def qr_generate():
    qr_code_data = random.randint(0, 100)
    save_qr_data(qr_code_data, qr_data_file)
    print(f"Generated QR Data: {qr_code_data}")

    qr_img = qrcode.make(qr_code_data)

    # Define file paths for saving QR code images
    qr_img_path_raspberry_pi = os.path.join(raspberry_pi_images_dir, "qr-img.jpg")
    qr_img_path_local = os.path.join(local_images_dir, "qr-img.jpg")

    # Save QR code images to both locations
    save_qr_image(qr_img, qr_img_path_raspberry_pi)
    save_qr_image(qr_img, qr_img_path_local)

def qr_generatepay():
    pay_data = random.randint(0, 100)
    save_qr_data(pay_data, pay_data_file)
    print(f"Generated Payment QR Data: {pay_data}")

    qr_img = qrcode.make(pay_data)

    # Define file paths for saving payment QR code images
    qr_img_path_raspberry_pi = os.path.join(raspberry_pi_images_dir, "qr-pay.jpg")
    qr_img_path_local = os.path.join(local_images_dir, "qr-pay.jpg")

    # Save payment QR code images to both locations
    save_qr_image(qr_img, qr_img_path_raspberry_pi)
    save_qr_image(qr_img, qr_img_path_local)

if __name__ == '__main__':
    qr_generate()
    qr_generatepay()
