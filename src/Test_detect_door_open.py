# Test_detect_door_open.py

import pytest
import queue
import time
from threading import Thread
from unittest.mock import MagicMock, patch

# Import the main function from the module
from detect_door_open import security, shared_keypad_queue

# Mock the hardware interaction modules
mock_led = MagicMock()
mock_adc = MagicMock()
mock_buzzer = MagicMock()
mock_keypad = MagicMock()
mock_ir_sensor = MagicMock()
mock_servo = MagicMock()
mock_lcd = MagicMock()

# Patch the hardware modules
@patch('detect_door_open.led', mock_led)
@patch('detect_door_open.adc', mock_adc)
@patch('detect_door_open.buzzer', mock_buzzer)
@patch('detect_door_open.keypad', mock_keypad)
@patch('detect_door_open.ir_sensor', mock_ir_sensor)
@patch('detect_door_open.servo', mock_servo)
@patch('detect_door_open.LCD.lcd', MagicMock(return_value=mock_lcd))
def test_security():
    # Mock behaviors
    mock_ir_sensor.get_ir_sensor_state.return_value = False
    mock_keypad.get_key = MagicMock(side_effect=lambda: time.sleep(0.1))

    def simulate_keypresses():
        # Simulate correct sequence 5, 6, 7
        time.sleep(0.2)
        shared_keypad_queue.put(5)
        time.sleep(0.2)
        shared_keypad_queue.put(6)
        time.sleep(0.2)
        shared_keypad_queue.put(7)
        time.sleep(0.2)
        shared_keypad_queue.put('*')

    # Start the security function in a separate thread
    security_thread = Thread(target=security)
    security_thread.start()

    # Simulate keypresses
    simulate_keypresses_thread = Thread(target=simulate_keypresses)
    simulate_keypresses_thread.start()

    # Give enough time for the sequence to process
    time.sleep(5)

    # Stop the threads after the test
    security_thread.join(timeout=1)
    simulate_keypresses_thread.join(timeout=1)

    # Assertions to verify the behavior
    mock_lcd.lcd_display_string.assert_any_call("Door Closed", 1)
    mock_lcd.lcd_display_string.assert_any_call("Authorization", 1)
    mock_lcd.lcd_display_string.assert_any_call("Granted", 2)
    mock_servo.set_servo_position.assert_any_call(90)
    mock_servo.set_servo_position.assert_any_call(0)
    mock_buzzer.beep.assert_called_with(1, 1, 3)
    mock_buzzer.turn_off.assert_called()

if __name__ == '__main__':
    pytest.main()
