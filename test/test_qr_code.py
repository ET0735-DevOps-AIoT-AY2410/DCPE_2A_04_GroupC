import pytest
import os
from test_cameradetect import qr_generate, qr_code_detection

@pytest.fixture(scope="module")
def setup_qr_code():
    # Define paths
    src_dir = os.path.join(os.getcwd(), "src")
    images_dir = os.path.join(src_dir, "images")
    qr_image_path = os.path.join(images_dir, "qr-code.jpg")
    
    # Ensure the images directory exists
    os.makedirs(images_dir, exist_ok=True)
    
    # Generate QR code if it does not exist
    if not os.path.exists(qr_image_path):
        qr_generate(qr_image_path)
    
    yield qr_image_path

def test_qr_code_detection(setup_qr_code):
    qr_image_path = setup_qr_code
    
    # Test QR code detection
    result = qr_code_detection(qr_image_path)
    
    # Assert the result is True
    assert result is True
