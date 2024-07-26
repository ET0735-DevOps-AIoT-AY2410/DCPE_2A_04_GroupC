from threading import Thread
import pytest
import time
from unittest.mock import MagicMock, patch
import force_detect

def test_monitor_accelerometer():
    # Mock the accelerometer readings to simulate 30g force
    with patch('hal.hal_accelerometer.ADXL345.get_3_axis', return_value=(30, 0, 0)):
        # Mock the buzzer beep method
        with patch('hal.hal_buzzer.beep') as mock_beep:
            # Run the monitor_accelerometer function in a thread for a short time
            def run_monitor():
                force_detect.monitor_accelerometer()
            
            monitor_thread = Thread(target=run_monitor)
            monitor_thread.start()
            time.sleep(0.2)  # Let the thread run for a short time
            monitor_thread.join(timeout=0.1)  # Ensure the thread stops

            # Check if the beep method was called
            assert mock_beep.called, "Buzzer should beep when total_g exceeds 20"

# Run the test
if __name__ == "__main__":
    pytest.main()
