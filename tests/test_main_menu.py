

import pytest
from unittest.mock import patch, Mock

# Import the main_menu function
from cli_menu.main_menu import main_menu

# Mock classes for StorageInterface and User
class MockStorageInterface(Mock):
    pass

class MockUser(Mock):
    def __init__(self, username="testuser", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username

@pytest.fixture
def mock_data_storage():
    """Fixture for a mock StorageInterface."""
    return MockStorageInterface()

@pytest.fixture
def mock_user():
    """Fixture for a mock User."""
    return MockUser("testuser")

# Test cases for main_menu
@patch('builtins.input', side_effect=['q'])
def test_main_menu_quit(mock_input, capsys, mock_data_storage, mock_user):
    main_menu(mock_data_storage, mock_user)
    captured = capsys.readouterr()
    output = captured.out
    assert f"--- Welcome, {mock_user.username}! ---" in output
    assert "Exiting program..." in output

@patch('builtins.input', side_effect=['invalid', 'q'])
def test_main_menu_invalid_input(mock_input, capsys, mock_data_storage, mock_user):
    main_menu(mock_data_storage, mock_user)
    captured = capsys.readouterr()
    output = captured.out
    assert "Invalid selection. Please try again." in output

@patch('cli_menu.main_menu.habit_tracking_menu')
@patch('builtins.input', side_effect=['1', 'q'])
def test_main_menu_option_1_habit_tracking(mock_input, mock_habit_tracking_menu, capsys, mock_data_storage, mock_user):
    main_menu(mock_data_storage, mock_user)
    captured = capsys.readouterr()
    output = captured.out
    assert "1: Habit tracking (track habit completion, add habits to tracking)" in output
    mock_habit_tracking_menu.assert_called_once_with(mock_data_storage, mock_user)

@patch('cli_menu.main_menu.habit_creation_menu')
@patch('builtins.input', side_effect=['2', 'q'])
def test_main_menu_option_2_habit_creation(mock_input, mock_habit_creation_menu, capsys, mock_data_storage, mock_user):
    main_menu(mock_data_storage, mock_user)
    captured = capsys.readouterr()
    output = captured.out
    assert "2: Habit creation (create new habits and edit existing ones)" in output
    mock_habit_creation_menu.assert_called_once_with(mock_data_storage)

@patch('cli_menu.main_menu.habit_analysis_menu')
@patch('builtins.input', side_effect=['3', 'q'])
def test_main_menu_option_3_habit_analysis(mock_input, mock_habit_analysis_menu, capsys, mock_data_storage, mock_user):
    main_menu(mock_data_storage, mock_user)
    captured = capsys.readouterr()
    output = captured.out
    assert "3: Habit analysis (view habit streaks)" in output
    mock_habit_analysis_menu.assert_called_once_with(mock_user)

