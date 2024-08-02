import pytest
from unittest.mock import MagicMock, patch

# Mock classes and functions
class MockSMBus:
    def __init__(self, i2c_port):
        pass

    def write_byte_data(self, i2c_address, register, value):
        pass

    def read_i2c_block_data(self, i2c_address, register, length):
        if register == 0x32:  # DATAX0 register
            return [0x00, 0x00, 0x00, 0x00, 0x00, 0x10]  # Example values
        return [0x00] * length

    def read_byte_data(self, i2c_address, register):
        if register == 0x30:  # INT_SOURCE register
            return 0x00  # Example data
        return 0x00

# Patch the imports and functions used in the force_detect module
@patch('force_detect.smbus2.SMBus', new=MockSMBus)
@patch('force_detect.acc.init', return_value=MagicMock())
@patch('force_detect.buzz.beep')
@patch('builtins.print')
def test_monitor_accelerometer(mock_print, mock_beep, mock_acc_init):
    # Mock the accelerometer's get_3_axis method to return fixed values
    mock_acc = mock_acc_init.return_value
    mock_acc.get_3_axis.return_value = (0.0, 0.0, 3.0)  # Simulate force detection

    # Import the module after patching
    import force_detect

    # Call the function to test
    force_detect.monitor_accelerometer()

    # Assertions
    mock_beep.assert_called_once_with(1, 1, 3)  # Ensure beep was called correctly
    assert any("Forced attempt to open Vending Machine" in call[0][0] for call in mock_print.call_args_list)

if __name__ == "__main__":
    pytest.main()
