# camera_module.py

import time
from picamera2 import Picamera2, Preview

def activate_camera(image_path):
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(
        main={"size": (1920, 1080)},
        lores={"size": (640, 480)},
        display="lores"
    )

    try:
        picam2.configure(camera_config)
        picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(2)
        picam2.capture_file(image_path)
        picam2.stop_preview()
        picam2.close()
        print(f"Image captured successfully at {image_path}")
    except Exception as e:
        print(f"Failed to capture image: {e}")
        picam2.close()
