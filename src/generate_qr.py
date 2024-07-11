# importing the qrcode library  
import qrcode  
import random
# generating a QR code using the make() function  
data = random.randint(0,100)
qr_img = qrcode.make(data)  
# saving the image file  
qr_img.save("qr-img.jpg")  