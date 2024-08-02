import pytest
from unittest.mock import MagicMock, call
from main_menu import display_menu, handle_user_selection, shared_keypad_queue

def test_display_menu():
    # Create a mock for the LCD
    lcd_mock = MagicMock()

    # Call the function with the mock
    display_menu(lcd_mock)

    # Assert the LCD displays were called with the expected strings
    lcd_mock.lcd_clear.assert_called_once()
    lcd_mock.lcd_display_string.assert_has_calls([
        call("1. Collect Drink", 1, 0),
        call("2. Purchase", 2, 0),
    ])

def test_handle_user_selection_option_1():
    # Create a mock for the LCD
    lcd_mock = MagicMock()

    # Simulate pressing key '1'
    shared_keypad_queue.put(1)

    # Call the function with the mock
    handle_user_selection(lcd_mock)

    # Assert the LCD displays were called with the expected strings for option 1
    lcd_mock.lcd_clear.assert_called_once()
    lcd_mock.lcd_display_string.assert_has_calls([
        call("Face QR Code", 1, 0),
        call("towards camera", 2, 0),
    ])

def test_handle_user_selection_option_2():
    # Create a mock for the LCD
    lcd_mock = MagicMock()

    # Simulate pressing key '2'
    shared_keypad_queue.put(2)

    # Call the function with the mock
    handle_user_selection(lcd_mock)

    # Assert the LCD displays were called with the expected strings for option 2
    lcd_mock.lcd_clear.assert_called_once()
    lcd_mock.lcd_display_string.assert_has_calls([
        call("1. Milo", 1, 0),
        call("2. 100 Plus", 2, 0),
    ])
