
import pytest
from unittest.mock import patch, Mock
from datetime import datetime

# Import the functions to be tested
from cli_menu.habit_analysis_menu import (
    habit_analysis_menu,
    show_all_habits_with_current_streak,
    show_all_habits_with_current_streak_for_specific_periodicity,
    get_habit_with_all_time_longest_streak,
    get_habit_with_current_longest_streak,
    get_current_streak_for_specific_habit,
    get_longest_all_time_streak_for_specific_habit,
)

# Mock classes for Habit and UserHabit
class MockHabit:
    def __init__(self, name, period="daily"):
        self.name = name
        self.period = period

class MockUserHabit:
    def __init__(self, habit, completion_times=None):
        self.habit = habit
        self.completion_times = completion_times if completion_times is not None else []

class MockUser:
    def __init__(self, username="testuser", habits=None):
        self.username = username
        self.habits = habits if habits is not None else []

@pytest.fixture
def mock_user_with_habits():
    # Setup mock habits and user for testing
    habit1 = MockHabit("Read", "daily")
    habit2 = MockHabit("Exercise", "weekly")
    habit3 = MockHabit("Meditate", "daily")

    user_habit1 = MockUserHabit(habit1, [datetime(2023, 1, 1), datetime(2023, 1, 2)])
    user_habit2 = MockUserHabit(habit2, [datetime(2023, 1, 1)])
    user_habit3 = MockUserHabit(habit3, [datetime(2023, 1, 1)])

    return MockUser("testuser", [user_habit1, user_habit2, user_habit3])

@pytest.fixture
def mock_analytics():
    with patch('cli_menu.habit_analysis_menu.analytics') as mock_analytics:
        yield mock_analytics

@patch('builtins.input', side_effect=['q'])
def test_habit_analysis_menu_quit(mock_input, capsys, mock_user_with_habits):
    habit_analysis_menu(mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Habit analysis ---" in output
    assert "1: Show all habits with current streak" in output
    assert "q: Return to main menu" in output

@patch('builtins.input', side_effect=['invalid', 'q'])
def test_habit_analysis_menu_invalid_input(mock_input, capsys, mock_user_with_habits):
    habit_analysis_menu(mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "Invalid input. Please try again." in output

@patch('builtins.input', side_effect=['1', 'q'])
def test_habit_analysis_menu_option_1(mock_input, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_all_tracked_habits_with_streak.return_value = [
        (mock_user_with_habits.habits[0].habit, 2)
    ]
    habit_analysis_menu(mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Habits with current streak ---" in output
    assert f"{mock_user_with_habits.habits[0].habit.name}: 2" in output

@patch('builtins.input', side_effect=['2', 'daily', 'q'])
def test_habit_analysis_menu_option_2(mock_input, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_all_tracked_habits_with_streak_for_periodicity.return_value = [
        (mock_user_with_habits.habits[0].habit, 2)
    ]
    habit_analysis_menu(mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Habits with current streak for specific periodicity ---" in output
    assert f"{mock_user_with_habits.habits[0].habit.name}: 2" in output

@patch('builtins.input', side_effect=['3', 'q'])
def test_habit_analysis_menu_option_3(mock_input, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_all_time_longest_habit_streak.return_value = (mock_user_with_habits.habits[0].habit, 10)
    habit_analysis_menu(mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Habit with all-time longest streak ---" in output
    assert f"{mock_user_with_habits.habits[0].habit.name}: 10" in output

@patch('builtins.input', side_effect=['4', 'q'])
def test_habit_analysis_menu_option_4(mock_input, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_current_longest_habit_streak.return_value = (mock_user_with_habits.habits[0].habit, 5)
    habit_analysis_menu(mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Habit with current longest streak ---" in output
    assert f"{mock_user_with_habits.habits[0].habit.name}: 5" in output

@patch('cli_menu.habit_analysis_menu.multi_page_option_selection_menu', side_effect=["Read"])
@patch('builtins.input', side_effect=['5', 'q'])
def test_habit_analysis_menu_option_5(mock_input, mock_multi_page_menu, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_current_streak_for_habit.return_value = 3
    habit_analysis_menu(mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Longest streak for specific habit ---" in output
    assert "Read: 3" in output

@patch('cli_menu.habit_analysis_menu.multi_page_option_selection_menu', side_effect=["Read"])
@patch('builtins.input', side_effect=['6', 'q'])
def test_habit_analysis_menu_option_6(mock_input, mock_multi_page_menu, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_longest_streak_for_habit.return_value = 12
    habit_analysis_menu(mock_user_with_habits)
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Longest all-time streak for specific habit ---" in output
    assert "Read: 12" in output

# Test helper functions directly
def test_show_all_habits_with_current_streak_no_habits(capsys, mock_analytics):
    mock_user = MockUser("testuser", [])
    mock_analytics.get_all_tracked_habits_with_streak.return_value = []
    show_all_habits_with_current_streak(mock_user)
    captured = capsys.readouterr()
    assert "No habits found for user." in captured.out

def test_show_all_habits_with_current_streak_with_habits(capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_all_tracked_habits_with_streak.return_value = [
        (mock_user_with_habits.habits[0].habit, 2),
        (mock_user_with_habits.habits[1].habit, 5)
    ]
    show_all_habits_with_current_streak(mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Read: 2" in captured.out
    assert "Exercise: 5" in captured.out

@patch('builtins.input', side_effect=['invalid_period', 'daily'])
def test_show_all_habits_with_current_streak_for_specific_periodicity(mock_input, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_all_tracked_habits_with_streak_for_periodicity.return_value = [
        (mock_user_with_habits.habits[0].habit, 2)
    ]
    show_all_habits_with_current_streak_for_specific_periodicity(mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Invalid period invalid_period. Please try again." in captured.out
    assert "Read: 2" in captured.out

def test_get_habit_with_all_time_longest_streak_no_habits(capsys, mock_analytics):
    mock_user = MockUser("testuser", [])
    mock_analytics.get_all_time_longest_habit_streak.return_value = (None, 0)
    get_habit_with_all_time_longest_streak(mock_user)
    captured = capsys.readouterr()
    assert "No habits found for user." in captured.out

def test_get_habit_with_all_time_longest_streak_with_habit(capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_all_time_longest_habit_streak.return_value = (mock_user_with_habits.habits[0].habit, 10)
    get_habit_with_all_time_longest_streak(mock_user_with_habits)
    captured = capsys.readouterr()
    assert f"{mock_user_with_habits.habits[0].habit.name}: 10" in captured.out

def test_get_habit_with_current_longest_streak_no_habits(capsys, mock_analytics):
    mock_user = MockUser("testuser", [])
    mock_analytics.get_current_longest_habit_streak.return_value = (None, 0)
    get_habit_with_current_longest_streak(mock_user)
    captured = capsys.readouterr()
    assert "No habits found for user." in captured.out

def test_get_habit_with_current_longest_streak_with_habit(capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_current_longest_habit_streak.return_value = (mock_user_with_habits.habits[0].habit, 5)
    get_habit_with_current_longest_streak(mock_user_with_habits)
    captured = capsys.readouterr()
    assert f"{mock_user_with_habits.habits[0].habit.name}: 5" in captured.out

@patch('cli_menu.habit_analysis_menu.multi_page_option_selection_menu', side_effect=["Read"])
def test_get_current_streak_for_specific_habit(mock_multi_page_menu, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_current_streak_for_habit.return_value = 3
    get_current_streak_for_specific_habit(mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Read: 3" in captured.out

@patch('cli_menu.habit_analysis_menu.multi_page_option_selection_menu', side_effect=["Read"])
def test_get_current_streak_for_specific_habit_no_selection(mock_multi_page_menu, capsys, mock_user_with_habits, mock_analytics):
    mock_multi_page_menu.return_value = None
    get_current_streak_for_specific_habit(mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Longest streak for specific habit" in captured.out # Title should still be printed
    assert "Read: 3" not in captured.out # Should not print streak if no selection

@patch('cli_menu.habit_analysis_menu.multi_page_option_selection_menu', side_effect=["Read"])
def test_get_longest_all_time_streak_for_specific_habit(mock_multi_page_menu, capsys, mock_user_with_habits, mock_analytics):
    mock_analytics.get_longest_streak_for_habit.return_value = 12
    get_longest_all_time_streak_for_specific_habit(mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Read: 12" in captured.out

@patch('cli_menu.habit_analysis_menu.multi_page_option_selection_menu', side_effect=["Read"])
def test_get_longest_all_time_streak_for_specific_habit_no_selection(mock_multi_page_menu, capsys, mock_user_with_habits, mock_analytics):
    mock_multi_page_menu.return_value = None
    get_longest_all_time_streak_for_specific_habit(mock_user_with_habits)
    captured = capsys.readouterr()
    assert "Longest all-time streak for specific habit" in captured.out # Title should still be printed
    assert "Read: 12" not in captured.out # Should not print streak if no selection

