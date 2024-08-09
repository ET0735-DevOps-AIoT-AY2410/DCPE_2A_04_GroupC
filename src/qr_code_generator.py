import qrcode
import random
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
