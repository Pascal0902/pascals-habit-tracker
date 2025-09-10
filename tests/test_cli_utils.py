
import pytest
from unittest.mock import patch
from cli_menu.cli_utils import multi_page_option_selection_menu

def test_multi_page_option_selection_menu_quit(capsys):
    with patch('builtins.input', side_effect=['q']):
        selection_name = "test option"
        options = ["option1", "option2"]
        
        result = multi_page_option_selection_menu(selection_name, options)
        
        assert result is None
        captured = capsys.readouterr()
        output = captured.out
        assert "--- Please select a test option ---" in output
        assert "1: option1" in output
        assert "2: option2" in output
        assert "q: Return to previous menu" in output
        assert "Page 1 / 1" in output

def test_multi_page_option_selection_menu_valid_selection(capsys):
    with patch('builtins.input', side_effect=['1']):
        selection_name = "test option"
        options = ["option1", "option2"]
        
        result = multi_page_option_selection_menu(selection_name, options)
        
        assert result == "option1"
        captured = capsys.readouterr()
        output = captured.out
        assert "1: option1" in output

def test_multi_page_option_selection_menu_invalid_selection_then_quit(capsys):
    with patch('builtins.input', side_effect=['99', 'q']):
        selection_name = "test option"
        options = ["option1", "option2"]
        
        result = multi_page_option_selection_menu(selection_name, options)
        
        assert result is None
        captured = capsys.readouterr()
        output = captured.out
        assert "Invalid selection. Please try again." in output

def test_multi_page_option_selection_menu_next_page(capsys):
    with patch('builtins.input', side_effect=['n', 'q']):
        options = [f"item{i}" for i in range(1, 15)] # 14 items, 9 per page -> 2 pages
        
        result = multi_page_option_selection_menu("items", options, page_number=0)
        
        assert result is None
        captured = capsys.readouterr()
        output = captured.out
        assert "Page 1 / 2" in output
        assert "Page 2 / 2" in output
        assert "n: Next page" in output
        assert "p: Previous page" in output # Should be present after going to next page
        assert "item1" in output
        assert "item10" in output

def test_multi_page_option_selection_menu_next_page_no_more_pages(capsys):
    with patch('builtins.input', side_effect=['n', 'q']):
        options = [f"item{i}" for i in range(1, 5)] # 4 items, 9 per page -> 1 page
        
        result = multi_page_option_selection_menu("items", options, page_number=0)
        
        assert result is None
        captured = capsys.readouterr()
        output = captured.out
        assert "Page 1 / 1" in output
        assert "No more pages. Please try again." in output

def test_multi_page_option_selection_menu_previous_page(capsys):
    with patch('builtins.input', side_effect=['p', 'q']):
        options = [f"item{i}" for i in range(1, 15)] # 14 items, 9 per page -> 2 pages
        
        result = multi_page_option_selection_menu("items", options, page_number=1)
        
        assert result is None
        captured = capsys.readouterr()
        output = captured.out
        assert "Page 2 / 2" in output
        assert "Page 1 / 2" in output
        assert "p: Previous page" in output
        assert "item1" in output
        assert "item10" in output

def test_multi_page_option_selection_menu_previous_page_no_previous_pages(capsys):
    with patch('builtins.input', side_effect=['p', 'q']):
        options = [f"item{i}" for i in range(1, 5)] # 4 items, 9 per page -> 1 page
        
        result = multi_page_option_selection_menu("items", options, page_number=0)
        
        assert result is None
        captured = capsys.readouterr()
        output = captured.out
        assert "Page 1 / 1" in output
        assert "No previous pages. Please try again." in output

def test_multi_page_option_selection_menu_select_on_second_page(capsys):
    with patch('builtins.input', side_effect=['n', '1']): # Go to next page, then select first item on second page
        options = [f"item{i}" for i in range(1, 15)]
        
        result = multi_page_option_selection_menu("items", options, page_number=0)
        
        assert result == "item10" # item 1 on second page is index 9 (item10)
        captured = capsys.readouterr()
        output = captured.out
        assert "Page 1 / 2" in output
        assert "Page 2 / 2" in output
        assert "1: item10" in output # Verify item on second page is displayed and selected

