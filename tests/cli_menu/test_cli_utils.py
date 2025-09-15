import pytest
import sys
import os
from unittest.mock import patch
from io import StringIO

# Add src to path for importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from cli_menu.cli_utils import multi_page_option_selection_menu


class TestCliUtils:
    """Test cases for CLI utility functions."""

    def test_multi_page_option_selection_menu_simple_selection(self):
        """Test selecting an option from a single page menu."""
        options = ["Option 1", "Option 2", "Option 3"]
        
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print') as mock_print:
                result = multi_page_option_selection_menu("option", options)
                
                assert result == "Option 2"
                # Verify menu was displayed
                mock_print.assert_any_call("--- Please select a option ---")
                mock_print.assert_any_call("1: Option 1")
                mock_print.assert_any_call("2: Option 2")
                mock_print.assert_any_call("3: Option 3")

    def test_multi_page_option_selection_menu_quit(self):
        """Test quitting from the menu."""
        options = ["Option 1", "Option 2"]
        
        with patch('builtins.input', return_value='q'):
            with patch('builtins.print'):
                result = multi_page_option_selection_menu("option", options)
                
                assert result is None

    def test_multi_page_option_selection_menu_invalid_selection_retry(self):
        """Test handling invalid selection and retrying."""
        options = ["Option 1", "Option 2"]
        
        # First invalid, then valid selection
        with patch('builtins.input', side_effect=['5', '1']):
            with patch('builtins.print') as mock_print:
                result = multi_page_option_selection_menu("option", options)
                
                assert result == "Option 1"
                # Should print error message
                mock_print.assert_any_call("Invalid selection. Please try again.")

    def test_multi_page_option_selection_menu_non_digit_invalid(self):
        """Test handling non-digit invalid input."""
        options = ["Option 1", "Option 2"]
        
        # First invalid, then valid selection
        with patch('builtins.input', side_effect=['invalid', '1']):
            with patch('builtins.print') as mock_print:
                result = multi_page_option_selection_menu("option", options)
                
                assert result == "Option 1"
                # Should print error message
                mock_print.assert_any_call("Invalid selection. Please try again.")

    def test_multi_page_option_selection_menu_multiple_pages(self):
        """Test menu with multiple pages."""
        # Create enough options for multiple pages (10+ options)
        options = [f"Option {i}" for i in range(1, 12)]
        
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print') as mock_print:
                result = multi_page_option_selection_menu("option", options)
                
                assert result == "Option 1"
                # Should show next/previous options
                mock_print.assert_any_call("n: Next page")
                mock_print.assert_any_call("p: Previous page")
                mock_print.assert_any_call("Page 1 / 2")

    def test_multi_page_option_selection_menu_next_page(self):
        """Test navigation to next page."""
        options = [f"Option {i}" for i in range(1, 12)]
        
        # Go to next page, then select option 1 (which should be Option 10)
        with patch('builtins.input', side_effect=['n', '1']):
            with patch('builtins.print') as mock_print:
                result = multi_page_option_selection_menu("option", options)
                
                assert result == "Option 10"  # First option on second page

    def test_multi_page_option_selection_menu_previous_page(self):
        """Test navigation to previous page."""
        options = [f"Option {i}" for i in range(1, 12)]
        
        # Start on page 1, go to next, then previous, then select
        with patch('builtins.input', side_effect=['n', 'p', '1']):
            with patch('builtins.print'):
                result = multi_page_option_selection_menu("option", options, 1)  # Start on page 1
                
                assert result == "Option 1"  # Back to first page

    def test_multi_page_option_selection_menu_invalid_next_page(self):
        """Test handling invalid next page navigation."""
        options = ["Option 1", "Option 2"]  # Only one page
        
        # Try to go to next page when there isn't one
        with patch('builtins.input', side_effect=['n', '1']):
            with patch('builtins.print') as mock_print:
                result = multi_page_option_selection_menu("option", options)
                
                assert result == "Option 1"
                # Should print error message
                mock_print.assert_any_call("No more pages. Please try again.")

    def test_multi_page_option_selection_menu_invalid_previous_page(self):
        """Test handling invalid previous page navigation."""
        options = [f"Option {i}" for i in range(1, 12)]
        
        # Try to go to previous page when on first page
        with patch('builtins.input', side_effect=['p', '1']):
            with patch('builtins.print') as mock_print:
                result = multi_page_option_selection_menu("option", options)
                
                assert result == "Option 1"
                # Should print error message
                mock_print.assert_any_call("No previous pages. Please try again.")

    def test_multi_page_option_selection_menu_page_calculation(self):
        """Test correct page calculation and display."""
        # Exactly 9 options should be 2 pages according to the algorithm
        options = [f"Option {i}" for i in range(1, 10)]
        
        with patch('builtins.input', return_value='q'):
            with patch('builtins.print') as mock_print:
                multi_page_option_selection_menu("option", options)
                
                # Should show page navigation since total_pages = 2
                assert any("n: Next page" in str(call) for call in mock_print.call_args_list)
                assert any("p: Previous page" in str(call) for call in mock_print.call_args_list)

    def test_multi_page_option_selection_menu_boundary_selection(self):
        """Test selecting the last option on a page."""
        options = [f"Option {i}" for i in range(1, 12)]
        
        # Select option 9 (last on first page)
        with patch('builtins.input', return_value='9'):
            with patch('builtins.print'):
                result = multi_page_option_selection_menu("option", options)
                
                assert result == "Option 9"

    def test_multi_page_option_selection_menu_empty_options(self):
        """Test menu with empty options list."""
        options = []
        
        with patch('builtins.input', return_value='q'):
            with patch('builtins.print') as mock_print:
                result = multi_page_option_selection_menu("option", options)
                
                assert result is None
                # Should still display menu structure
                mock_print.assert_any_call("--- Please select a option ---")


if __name__ == '__main__':
    pytest.main([__file__])