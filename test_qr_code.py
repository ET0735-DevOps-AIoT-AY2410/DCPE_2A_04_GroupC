# test_qr_code.py
import pytest
from unittest.mock import patch, MagicMock
from cameradetect import activate_camera, check_qr_code, dispense_drink, qr_code_detection, main
from qr_code_generator import qr_generate

image_path = r'/mnt/data/test.jpg'
font_path = r'/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'

def test_activate_camera():
    with patch('cameradetect.activate_camera') as mock_activate_camera:
        mock_activate_camera.return_value = None
        activate_camera(image_path)
        mock_activate_camera.assert_called_once_with(image_path)

def test_check_qr_code():
    # Mock qr_data for testing
    mock_qr_data = 'test_qr_code'
    with patch('cameradetect.qr_data', mock_qr_data):
        assert check_qr_code('test_qr_code') == True
        assert check_qr_code('invalid_code') == False

def test_dispense_drink(capsys):
    dispense_drink()
    captured = capsys.readouterr()
    assert "Dispensing purchased drink" in captured.out

def test_qr_code_detection():
    with patch('cameradetect.Image.open') as mock_open, \
         patch('cameradetect.decode') as mock_decode:
        mock_img = MagicMock()
        mock_open.return_value = mock_img
        mock_decode.return_value = [MagicMock(data=b'test_qr_code', rect=MagicMock(left=0, top=0, width=100, height=100), polygon=[(0, 0), (100, 0), (100, 100), (0, 100)])]
        
        with patch('cameradetect.check_qr_code', return_value=True) as mock_check_qr_code, \
             patch('cameradetect.dispense_drink') as mock_dispense_drink:
            qr_code_detection(image_path, font_path)
            mock_check_qr_code.assert_called_once_with('test_qr_code')
            mock_dispense_drink.assert_called_once()

def test_main():
    with patch('cameradetect.qr_generate') as mock_qr_generate, \
         patch('cameradetect.activate_camera') as mock_activate_camera, \
         patch('cameradetect.qr_code_detection') as mock_qr_code_detection:
        mock_qr_generate.return_value = None
        mock_activate_camera.return_value = None
        mock_qr_code_detection.return_value = None

        main(image_path, font_path)
        mock_qr_generate.assert_called_once()
        mock_activate_camera.assert_called_once_with(image_path)
        mock_qr_code_detection.assert_called_once_with(image_path, font_path)

if __name__ == '__main__':
    pytest.main()
