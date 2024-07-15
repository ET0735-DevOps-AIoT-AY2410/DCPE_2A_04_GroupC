def dispense_drink():
    print("Dispense selected drink")

def face_qr_towards_camera():
    print("Face QR Code Towards Camera")

def tap_card():
    print("Tap Card")

def camera_activates():
    print("Camera activates")

def rfid_reader_activates():
    print("RFID Card Reader activates")

def user_selects_drink():
    print("Select drink:\n1. Milo\n2. 100 Plus")
    drink = input("Enter your choice (1 or 2): ")
    return drink

def user_selects_payment_method():
    print("Select payment method:\n1. Card\n2. App")
    method = input("Enter your choice (1 or 2): ")
    return method

def qr_code_shown():
    response = input("Is QR Code shown? (yes or no): ").lower()
    return response == "yes"

def qr_code_correct():
    response = input("Is the QR Code correct? (yes or no): ").lower()
    return response == "yes"

def payment_successful():
    response = input("Did the payment go through? (yes or no): ").lower()
    return response == "yes"

def main():
    drink = user_selects_drink()
    
    if drink not in ["1", "2"]:
        print("Invalid selection. Restarting...")
        return
    
    payment_method = user_selects_payment_method()
    
    if payment_method == "2":  # App
        camera_activates()
        face_qr_towards_camera()
        
        if not qr_code_shown():
            print("QR Code not shown. Restarting...")
            return
        
        if not qr_code_correct():
            print("QR Code incorrect. Restarting...")
            return
        
        
        dispense_drink()
    
    elif payment_method == "1":  # Card
        rfid_reader_activates()
        tap_card()
        
        if not payment_successful():
            print("Payment failed. Restarting...")
            return
        
        dispense_drink()
    
    else:
        print("Invalid payment method. Restarting...")
        return

if __name__ == "__main__":
    main()
