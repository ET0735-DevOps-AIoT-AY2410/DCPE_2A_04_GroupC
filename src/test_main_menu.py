import pytest
from unittest.mock import patch
import main_menu

def test_main_menu_option():
    with patch('main_menu.handle_user_selection') as mock_menu_function:
        # Mock the return value of the menu function
        mock_menu_function.return_value = "expected outcome"
        
        # Call the function you're testing
        result = main_menu.handle_user_selection()
        
        # Assert that the function returns the expected outcome
        assert result == "expected outcome"
