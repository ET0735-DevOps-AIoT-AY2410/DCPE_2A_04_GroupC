import qrcode
import random
import qr_code_data

def qr_generate():
    qr_code_data.qr_data = random.randint(0, 100)
    print(f"Generated QR Data: {qr_code_data.qr_data}")
    qr_img = qrcode.make(qr_code_data.qr_data)
    qr_img.save("qr-img.jpg")

def qr_generatepay():
    qr_code_data.qr_data = random.randint(0, 100)
    print(f"Generated QR Data: {qr_code_data.qr_data}")
    qr_img = qrcode.make(qr_code_data.qr_data)
    qr_img.save("qr-pay.jpg")

if __name__ == '__main__':
    qr_generate()
    qr_generatepay()