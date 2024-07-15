import qrcode  
import random

# Define qr_data at the module level
qr_data = None

def qr_generate():
    global qr_data  # Use the global keyword to modify the module-level qr_data
    qr_data = random.randint(0, 100)
    print(f"Generated QR Data: {qr_data}")
    qr_img = qrcode.make(qr_data)  
    qr_img.save("qr-img.jpg")  

def qr_generate_2():
    data = random.randint(0, 100)
    qr_img = qrcode.make(data)  
    qr_img.save("qr-payment.jpg")  

if __name__ == '__main__':
    qr_generate()
    qr_generate_2()

