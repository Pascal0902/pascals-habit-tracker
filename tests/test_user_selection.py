

import pytest
from unittest.mock import patch, Mock

# Import the functions to be tested
from cli_menu.user_selection import (
    user_menu_main,
    user_login,
    create_user,
)

# Mock classes for StorageInterface and User
class MockStorageInterface(Mock):
    pass

class MockUser(Mock):
    def __init__(self, username="testuser", habits=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.habits = habits if habits is not None else []

@pytest.fixture
def mock_data_storage():
    """Fixture for a mock StorageInterface."""
    return MockStorageInterface()

@pytest.fixture
def mock_user():
    """Fixture for a mock User."""
    return MockUser("testuser")

# Test cases for user_menu_main
@patch('builtins.input', side_effect=['q'])
def test_user_menu_main_quit(mock_input, capsys, mock_data_storage):
    result = user_menu_main(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Please select an option ---" in output
    assert "q: Exit program" in output
    assert "Exiting program..." in output
    assert result is None

@patch('builtins.input', side_effect=['invalid', 'q'])
def test_user_menu_main_invalid_input(mock_input, capsys, mock_data_storage):
    result = user_menu_main(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "Invalid selection. Please try again." in output
    assert "Exiting program..." in output
    assert result is None

@patch('cli_menu.user_selection.user_login')
@patch('builtins.input', side_effect=['1'])
def test_user_menu_main_option_1_calls_user_login(mock_input, mock_user_login, capsys, mock_data_storage):
    user_menu_main(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "1: Login with existing account" in output
    mock_user_login.assert_called_once_with(mock_data_storage)

@patch('cli_menu.user_selection.create_user')
@patch('builtins.input', side_effect=['2'])
def test_user_menu_main_option_2_calls_create_user(mock_input, mock_create_user, capsys, mock_data_storage):
    user_menu_main(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "2: Create a new account" in output
    mock_create_user.assert_called_once_with(mock_data_storage)

# Test cases for user_login
@patch('cli_menu.user_selection.user_menu_main')
@patch('builtins.input', side_effect=['q'])
def test_user_login_quit(mock_input, mock_user_menu_main, capsys, mock_data_storage):
    user_login(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Please enter your username ---" in output
    mock_user_menu_main.assert_called_once_with(mock_data_storage)

@patch('cli_menu.user_selection.user_login')
@patch('cli_menu.user_selection.main_menu')
@patch('builtins.input', side_effect=['nonexistent_user', 'q'])
def test_user_login_user_not_found(mock_input, mock_main_menu, mock_user_login_recursive_call, capsys, mock_data_storage, mock_user):
    mock_data_storage.get_user.side_effect = [None, mock_user] # First call: user not found, second call from recursion exits with 'q'
    user_login(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "User not found. Please try again." in output
    mock_data_storage.get_user.assert_called_with("nonexistent_user")
    assert mock_data_storage.get_user.call_count == 1 # Only called once before 'q' exits recursion
    mock_main_menu.assert_not_called()

@patch('cli_menu.user_selection.main_menu')
@patch('builtins.input', side_effect=['existing_user'])
def test_user_login_success(mock_input, mock_main_menu, capsys, mock_data_storage, mock_user):
    mock_data_storage.get_user.return_value = mock_user
    user_login(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Please enter your username ---" in output
    mock_data_storage.get_user.assert_called_once_with("existing_user")
    mock_main_menu.assert_called_once_with(mock_data_storage, mock_user)

# Test cases for create_user
@patch('cli_menu.user_selection.user_menu_main')
@patch('builtins.input', side_effect=['q'])
def test_create_user_quit(mock_input, mock_user_menu_main, capsys, mock_data_storage):
    create_user(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Please enter your username ---" in output
    mock_user_menu_main.assert_called_once_with(mock_data_storage)

@patch('cli_menu.user_selection.main_menu')
@patch('cli_menu.user_selection.create_user')
@patch('builtins.input', side_effect=['existing_username', 'q']) # Try to create existing, then quit
def test_create_user_username_exists(mock_input, mock_create_user_recursive_call, mock_main_menu, capsys, mock_data_storage):
    mock_data_storage.insert_user.side_effect = [False, True] # First call fails (exists), second call from recursion is mocked by 'q'
    
    # We also need to mock the User constructor for the second recursive call if it were to proceed,
    # but since 'q' interrupts, we don't need a full User mock for the second attempt.
    # The actual call to create_user in the original logic would eventually create a User object if not 'q'.
    
    with patch('cli_menu.user_selection.User') as MockUserConstructor:
        # Create a mock user that will be returned by the mocked User constructor
        mock_user_instance = MockUser(username="existing_username", habits=[])
        MockUserConstructor.return_value = mock_user_instance
        
        create_user(mock_data_storage)
        captured = capsys.readouterr()
        output = captured.out
        assert "Username already exists. Please try again." in output
        # Assert that insert_user was called with the mock user instance
        mock_data_storage.insert_user.assert_called_with(mock_user_instance)
        assert mock_data_storage.insert_user.call_count == 1 # Only called once before 'q' exits recursion
        mock_main_menu.assert_not_called()

@patch('cli_menu.user_selection.main_menu')
@patch('builtins.input', side_effect=['new_username'])
def test_create_user_success(mock_input, mock_main_menu, capsys, mock_data_storage, mock_user):
    mock_data_storage.insert_user.return_value = True
    with patch('cli_menu.user_selection.User', return_value=mock_user) as MockUserConstructor:
        create_user(mock_data_storage)
        captured = capsys.readouterr()
        output = captured.out
        assert "--- Please enter your username ---" in output
        MockUserConstructor.assert_called_once_with(username="new_username", habits=[])
        mock_data_storage.insert_user.assert_called_once_with(mock_user)
        mock_main_menu.assert_called_once_with(mock_data_storage, mock_user)


