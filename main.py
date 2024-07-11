import cv2
import picamera2
def activate_camera():
    print("Activating camera")
    from picamera2 import Picamera2, Preview
    import time

    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(
        main={"size": (1920, 1080)},
        lores={"size": (640, 480)},
        display="lores"
    )
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("test.jpg")
    print("Camera activated and image captured")
    picam2.stop_preview()
    picam2.close()

def check_qr_code(data):
    return data == "valid_code"

def dispense_drink():
    print("Dispensing purchased drink")


def qr_code_detection():
    print('Face QR Code Towards Camera')
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)

        if bbox is not None:
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 255), thickness=2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            if data:
                print("QR Code detected: ", data)
                if check_qr_code(data):
                    dispense_drink()
                    break
                else:
                    print("Invalid QR Code. Please try again.")
        else:
            print("No QR code shown. Please face the QR code towards the camera.")

        cv2.imshow("code detector", img)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    activate_camera()
    qr_code_detection()

if _name_ == "_main_":
    main()






if __name__ == '__main__':
    main()