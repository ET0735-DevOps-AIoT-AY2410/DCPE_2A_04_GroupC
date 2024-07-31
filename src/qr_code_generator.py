import qrcode
import random
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
=======
import qr_code_data
>>>>>>> ervin

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
<<<<<<< HEAD
    qr_generate_2()
=======
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
    qr_generatepay()  # Corrected function call
>>>>>>> jiasheng
=======
    qr_generatepay()
>>>>>>> ervin
