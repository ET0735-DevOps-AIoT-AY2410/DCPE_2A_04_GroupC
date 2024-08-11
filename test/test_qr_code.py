import pytest
import os
from test_cameradetect import qr_generate, qr_code_detection

@pytest.fixture(scope="module")
def setup_qr_code():
    qr_image_path = "src/qr-code.jpg"
    if not os.path.exists(qr_image_path):
        qr_generate(qr_image_path)
    yield qr_image_path
    # Cleanup if necessary (delete the image file, etc.)

def test_qr_code_detection(setup_qr_code):
    qr_image_path = setup_qr_code
    
    result = qr_code_detection(qr_image_path)
    
    assert result is True
