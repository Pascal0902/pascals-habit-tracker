

import pytest
from unittest.mock import patch, Mock
from datetime import datetime

# Import the functions to be tested
from cli_menu.habit_creation_menu import (
    habit_creation_menu,
    create_new_habit,
    edit_existing_habit,
    delete_existing_habit,
)
from habit_tracking.habits import Habit

# Mock classes for Habit and UserHabit (similar to test_habit_analysis_menu.py)
class MockHabit:
    def __init__(self, name, task_description="desc", period="daily", creation_time=None):
        self.name = name
        self.task_description = task_description
        self.period = period
        self.creation_time = creation_time if creation_time else datetime.now()

class MockUserHabit:
    def __init__(self, habit, userhabit_id="uhid1", completion_times=None, creation_time=None):
        self.habit = habit
        self.userhabit_id = userhabit_id
        self.completion_times = completion_times if completion_times is not None else []
        self.creation_time = creation_time if creation_time else datetime.now()

@pytest.fixture
def mock_data_storage():
    """Fixture for a mock StorageInterface."""
    mock_storage = Mock()
    mock_storage.get_all_habits.return_value = []
    mock_storage.get_all_user_habits.return_value = []
    mock_storage.get_habit.return_value = None
    return mock_storage

@pytest.fixture
def existing_habit():
    """Fixture for an existing mock habit."""
    return MockHabit("Existing Habit", "Do something", "daily")

@pytest.fixture
def existing_user_habit(existing_habit):
    """Fixture for an existing mock user habit tracking the existing_habit."""
    return MockUserHabit(existing_habit)

# Test cases for habit_creation_menu
@patch('builtins.input', side_effect=['q'])
def test_habit_creation_menu_quit(mock_input, capsys, mock_data_storage):
    habit_creation_menu(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Habit creation ---" in output
    assert "1: Create new habit" in output
    assert "q: Return to main menu" in output

@patch('builtins.input', side_effect=['invalid', 'q'])
def test_habit_creation_menu_invalid_input(mock_input, capsys, mock_data_storage):
    habit_creation_menu(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "Invalid input. Please try again." in output

# Test cases for create_new_habit
@patch('builtins.input', side_effect=['New Habit', 'New Description', 'daily'])
def test_create_new_habit_success(mock_input, capsys, mock_data_storage):
    create_new_habit(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Create new habit ---" in output
    assert "New Habit created." in output
    mock_data_storage.insert_habit.assert_called_once()
    assert isinstance(mock_data_storage.insert_habit.call_args[0][0], Habit)
    assert mock_data_storage.insert_habit.call_args[0][0].name == "New Habit"

@patch('builtins.input', side_effect=['Existing Habit', 'New Habit', 'New Description', 'daily'])
def test_create_new_habit_already_exists(mock_input, capsys, mock_data_storage, existing_habit):
    mock_data_storage.get_habit.side_effect = [existing_habit, None] # First call returns existing, second returns None
    create_new_habit(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "Habit with that name already exists. Please try again." in output
    assert "New Habit created." in output
    # Ensure get_habit was called twice (once for initial check, once for recursive call)
    assert mock_data_storage.get_habit.call_count == 2
    mock_data_storage.insert_habit.assert_called_once()
    assert isinstance(mock_data_storage.insert_habit.call_args[0][0], Habit)
    assert mock_data_storage.insert_habit.call_args[0][0].name == "New Habit"

@patch('builtins.input', side_effect=['Test Habit', 'Test Description', 'invalid', 'daily'])
def test_create_new_habit_invalid_period(mock_input, capsys, mock_data_storage):
    create_new_habit(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "Invalid period invalid. Please try again." in output
    assert "Test Habit created." in output
    mock_data_storage.insert_habit.assert_called_once()
    assert mock_data_storage.insert_habit.call_args[0][0].period == "daily"

# Test cases for edit_existing_habit
@patch('cli_menu.habit_creation_menu.multi_page_option_selection_menu', return_value=None)
def test_edit_existing_habit_no_selection(mock_multi_page, capsys, mock_data_storage):
    edit_existing_habit(mock_data_storage)
    captured = capsys.readouterr()
    assert "--- Edit existing habit ---" in captured.out
    mock_data_storage.update_habit.assert_not_called()

@patch('cli_menu.habit_creation_menu.multi_page_option_selection_menu', return_value="Existing Habit")
@patch('builtins.input', side_effect=['Updated Description'])
def test_edit_existing_habit_success(mock_input, mock_multi_page, capsys, mock_data_storage, existing_habit):
    mock_data_storage.get_all_habits.return_value = [existing_habit]
    mock_data_storage.get_habit.return_value = existing_habit
    edit_existing_habit(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "Current task description: Do something" in output
    assert "Existing Habit updated." in output
    mock_data_storage.update_habit.assert_called_once_with(existing_habit)
    assert existing_habit.task_description == "Updated Description"

# Test cases for delete_existing_habit
@patch('cli_menu.habit_creation_menu.multi_page_option_selection_menu', return_value=None)
def test_delete_existing_habit_no_selection(mock_multi_page, capsys, mock_data_storage):
    delete_existing_habit(mock_data_storage)
    captured = capsys.readouterr()
    assert "--- Delete existing habit ---" in captured.out
    mock_data_storage.delete_habit.assert_not_called()

@patch('cli_menu.habit_creation_menu.multi_page_option_selection_menu', return_value="Existing Habit")
def test_delete_existing_habit_success(mock_multi_page, capsys, mock_data_storage, existing_habit):
    mock_data_storage.get_all_habits.return_value = [existing_habit]
    mock_data_storage.get_habit.return_value = existing_habit
    mock_data_storage.get_all_user_habits.return_value = [] # No user habits tracking it
    delete_existing_habit(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "Existing Habit deleted." in output
    mock_data_storage.delete_habit.assert_called_once_with(existing_habit)

@patch('cli_menu.habit_creation_menu.multi_page_option_selection_menu', return_value="Existing Habit")
def test_delete_existing_habit_tracked_by_user(mock_multi_page, capsys, mock_data_storage, existing_habit, existing_user_habit):
    mock_data_storage.get_all_habits.return_value = [existing_habit]
    mock_data_storage.get_habit.return_value = existing_habit
    mock_data_storage.get_all_user_habits.return_value = [existing_user_habit] # Habit is being tracked
    delete_existing_habit(mock_data_storage)
    captured = capsys.readouterr()
    output = captured.out
    assert "Existing Habit is currently being tracked by users. Please remove it from tracking before deleting." in output
    mock_data_storage.delete_habit.assert_not_called()

