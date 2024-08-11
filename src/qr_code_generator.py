import qrcode
import random
<<<<<<< HEAD
<<<<<<< HEAD

<<<<<<< HEAD
qr_data_file = "qr_data.txt"
pay_data_file = "pay_data.txt"

def save_qr_data(data):
    with open(qr_data_file, "w") as file:
        file.write(str(data))

def save_pay_data(data2):
    with open(pay_data_file, "w") as file:
        file.write(str(data2))

def qr_generate():
    qr_data = random.randint(0, 100)
    save_qr_data(qr_data)
    print(f"Generated QR Data: {qr_data}")
    qr_img = qrcode.make(qr_data)
    qr_img.save("qr-img.jpg")

def qr_generate_2():
    pay_data = random.randint(0,100)
    save_pay_data(pay_data)
    print(f"Generated QR Data: {pay_data}")
    qr_img = qrcode.make(pay_data)  
    qr_img.save("qr-payment.jpg") 

if __name__ == '__main__':
    qr_generate()
    qr_generate_2()
=======
import qr_code_data
=======
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
>>>>>>> jiasheng

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
<<<<<<< HEAD
    qr_generatepay()  # Corrected function call
>>>>>>> jiasheng
=======
    qr_generatepay()
>>>>>>> jiasheng
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

if __name__ == '__main__':
    qr_generate()
    qr_generatepay()
>>>>>>> cb93a8ad2beb5af31f1fe8f44aceb936f052ea21
