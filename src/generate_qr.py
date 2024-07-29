import qrcode
import random

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
