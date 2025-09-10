
import pytest
from unittest.mock import patch, Mock
from datetime import datetime, date
import re

# Import the functions to be tested
from cli_menu.habit_tracking_menu import (
    habit_tracking_menu,
    track_habit_completion,
    add_habit_to_tracking,
    remove_habit_from_tracking,
)

# Mock classes for Habit and UserHabit
class MockHabit:
    def __init__(self, name, period="daily", creation_time=None):
        self.name = name
        self.period = period
        self.creation_time = creation_time if creation_time else datetime(2023, 1, 1)

class MockUserHabit:
    def __init__(self, habit, completion_times=None, creation_time=None):
        self.habit = habit
        self.completion_times = completion_times if completion_times is not None else []
        self.creation_time = creation_time if creation_time else datetime(2023, 1, 1)
    
    def track_completion(self, completion_time=None):
        # This mock method will be patched further in tests when specific behavior is needed.
        # Default behavior: append current datetime or the provided completion_time.
        if completion_time:
            self.completion_times.append(completion_time)
        else:
            self.completion_times.append(datetime.now())

class MockUser:
    def __init__(self, username="testuser", habits=None):
        self.username = username
        self.habits = habits if habits is not None else []

    def add_habit(self, habit):
        user_habit = MockUserHabit(habit)
        self.habits.append(user_habit)
        return user_habit

    def remove_habit(self, habit):
        for i, uh in enumerate(self.habits):
            if uh.habit.name == habit.name:
                return self.habits.pop(i)
        return None


@pytest.fixture
def mock_data_storage():
    """Fixture for a mock StorageInterface."""
    mock_storage = Mock()
    mock_storage.get_all_habits.return_value = []
    mock_storage.get_habit.return_value = None
    return mock_storage

@pytest.fixture
def mock_user_with_habits():
    """Fixture for a mock User with some habits."""
    habit1 = MockHabit("Read", creation_time=datetime(2023,1,1))
    habit2 = MockHabit("Exercise", creation_time=datetime(2023,2,1))
    user_habit1 = MockUserHabit(habit1, creation_time=datetime(2023,1,1))
    user_habit2 = MockUserHabit(habit2, creation_time=datetime(2023,2,1))
    return MockUser("testuser", [user_habit1, user_habit2])

@pytest.fixture
def mock_empty_user():
    """Fixture for a mock User with no habits."""
    return MockUser("emptyuser", [])

# Test cases for habit_tracking_menu
@patch('builtins.input', side_effect=['q'])
def test_habit_tracking_menu_quit(mock_input, capsys, mock_data_storage, mock_user_with_habits):
    habit_tracking_menu(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Habit tracking ---" in output
    assert "1: Track habit completion" in output
    assert "q: Return to main menu" in output

@patch('builtins.input', side_effect=['invalid', 'q'])
def test_habit_tracking_menu_invalid_input(mock_input, capsys, mock_data_storage, mock_user_with_habits):
    habit_tracking_menu(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "Invalid selection. Please try again." in output

# Test cases for track_habit_completion
@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value=None)
def test_track_habit_completion_no_selection(mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    track_habit_completion(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    assert "--- Track habit completion ---" in captured.out
    mock_data_storage.update_user_habit.assert_not_called()

def test_track_habit_completion_no_habits_to_track(capsys, mock_data_storage, mock_empty_user):
    track_habit_completion(mock_data_storage, mock_empty_user)
    captured = capsys.readouterr()
    assert "No habits to track. Please add a habit to tracking first." in captured.out
    mock_data_storage.update_user_habit.assert_not_called()

@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value="Read")
@patch('builtins.input', side_effect=['']) # Press enter for today
@patch('cli_menu.habit_tracking_menu.datetime', autospec=True)
def test_track_habit_completion_today(mock_datetime_module, mock_input, mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    mock_now = datetime(2023, 3, 10)
    mock_datetime_module.now.return_value = mock_now
    mock_datetime_module.strptime = datetime.strptime # Ensure strptime works normally

    # Directly mock the track_completion method's behavior for this specific test
    with patch.object(mock_user_with_habits.habits[0], 'track_completion') as mock_track_completion:
        def side_effect_track_completion(completion_time=None):
            if completion_time:
                mock_user_with_habits.habits[0].completion_times.append(completion_time)
            else:
                mock_user_with_habits.habits[0].completion_times.append(mock_now)
        mock_track_completion.side_effect = side_effect_track_completion

        track_habit_completion(mock_data_storage, mock_user_with_habits)
        captured = capsys.readouterr()
        output = captured.out
        assert "Read marked as completed for today." in output
        mock_data_storage.update_user_habit.assert_called_once()
        mock_track_completion.assert_called_once_with() # Ensure it's called without explicit time
        assert mock_user_with_habits.habits[0].completion_times[-1].date() == mock_now.date() # Check against mocked now

@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value="Read")
@patch('builtins.input', side_effect=['q']) # Return to menu
def test_track_habit_completion_return_to_menu(mock_input, mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    track_habit_completion(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Read marked as completed for today." not in captured.out
    mock_data_storage.update_user_habit.assert_not_called()

@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value="Read")
@patch('builtins.input', side_effect=['2023-02-15'])
@patch('cli_menu.habit_tracking_menu.datetime', autospec=True)
def test_track_habit_completion_specific_date_success(mock_datetime_module, mock_input, mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    mock_now = datetime(2023, 3, 10)
    mock_datetime_module.now.return_value = mock_now
    mock_datetime_module.strptime = datetime.strptime # Ensure strptime works normally
    # mock_datetime_module.fromisoformat = datetime.fromisoformat # Not directly used in the module for this path

    track_habit_completion(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "Read marked as completed for 2023-02-15." in output
    mock_data_storage.update_user_habit.assert_called_once()
    assert mock_user_with_habits.habits[0].completion_times[-1].date() == date(2023, 2, 15)

@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value="Read")
@patch('builtins.input', side_effect=['2024-01-01', 'q']) # Future date, then quit
@patch('cli_menu.habit_tracking_menu.datetime', autospec=True)
def test_track_habit_completion_future_date(mock_datetime_module, mock_input, mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    mock_now = datetime(2023, 3, 10)
    mock_datetime_module.now.return_value = mock_now
    mock_datetime_module.strptime = datetime.strptime
    # mock_datetime_module.fromisoformat = datetime.fromisoformat

    track_habit_completion(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Cannot mark a habit as completed for a future date. Please try again." in captured.out
    mock_data_storage.update_user_habit.assert_not_called() # Should not update on invalid date

@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value="Read")
@patch('builtins.input', side_effect=['2022-12-01', 'q']) # Before creation date (2023-01-01), then quit
@patch('cli_menu.habit_tracking_menu.datetime', autospec=True)
def test_track_habit_completion_before_creation_date(mock_datetime_module, mock_input, mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    mock_now = datetime(2023, 3, 10)
    mock_datetime_module.now.return_value = mock_now
    mock_datetime_module.strptime = datetime.strptime
    # mock_datetime_module.fromisoformat = datetime.fromisoformat

    track_habit_completion(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Cannot mark a habit as completed before the habit was started. Please try again." in captured.out
    mock_data_storage.update_user_habit.assert_not_called()

@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value="Read")
@patch('builtins.input', side_effect=['invalid-date-format', 'q']) # Invalid format, then quit
@patch('cli_menu.habit_tracking_menu.datetime', autospec=True)
def test_track_habit_completion_invalid_date_format(mock_datetime_module, mock_input, mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    mock_now = datetime(2023, 3, 10)
    mock_datetime_module.now.return_value = mock_now
    mock_datetime_module.strptime = datetime.strptime
    # mock_datetime_module.fromisoformat = datetime.fromisoformat

    track_habit_completion(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Invalid input. Please try again." in captured.out
    mock_data_storage.update_user_habit.assert_not_called()

# Test cases for add_habit_to_tracking
@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value=None)
def test_add_habit_to_tracking_no_selection(mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    add_habit_to_tracking(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    assert "--- Add habit to tracking ---" in captured.out
    mock_data_storage.insert_user_habit.assert_not_called()
    mock_data_storage.update_user.assert_not_called()

@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value="New Habit")
def test_add_habit_to_tracking_success(mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    new_habit = MockHabit("New Habit")
    mock_data_storage.get_all_habits.return_value = [new_habit]
    mock_data_storage.get_habit.return_value = new_habit

    initial_habit_count = len(mock_user_with_habits.habits)
    add_habit_to_tracking(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "New Habit added to tracking." in output
    assert len(mock_user_with_habits.habits) == initial_habit_count + 1
    mock_data_storage.insert_user_habit.assert_called_once()
    mock_data_storage.update_user.assert_called_once()
    assert mock_user_with_habits.habits[-1].habit.name == "New Habit"

# Test cases for remove_habit_from_tracking
@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value=None)
def test_remove_habit_from_tracking_no_selection(mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    remove_habit_from_tracking(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    assert "--- Remove habit from tracking ---" in captured.out
    mock_data_storage.delete_user_habit.assert_not_called()
    mock_data_storage.update_user.assert_not_called()

def test_remove_habit_from_tracking_no_habits_to_remove(capsys, mock_data_storage, mock_empty_user):
    remove_habit_from_tracking(mock_data_storage, mock_empty_user)
    captured = capsys.readouterr()
    assert "No habits to remove from tracking." in captured.out
    mock_data_storage.delete_user_habit.assert_not_called()
    mock_data_storage.update_user.assert_not_called()

@patch('cli_menu.habit_tracking_menu.multi_page_option_selection_menu', return_value="Read")
def test_remove_habit_from_tracking_success(mock_multi_page_menu, capsys, mock_data_storage, mock_user_with_habits):
    mock_data_storage.get_habit.return_value = mock_user_with_habits.habits[0].habit # Return the "Read" habit

    initial_habit_count = len(mock_user_with_habits.habits)
    remove_habit_from_tracking(mock_data_storage, mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "Read removed from tracking." in output
    assert len(mock_user_with_habits.habits) == initial_habit_count - 1
    mock_data_storage.delete_user_habit.assert_called_once()
    mock_data_storage.update_user.assert_called_once()
