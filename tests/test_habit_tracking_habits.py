

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from src.habit_tracking.habits import Habit, UserHabit

@pytest.fixture
def daily_habit():
    return Habit("Daily Read", "Read a book daily", "daily", datetime(2023, 1, 1, 10, 0, 0))

@pytest.fixture
def weekly_habit():
    return Habit("Weekly Exercise", "Exercise 3 times a week", "weekly", datetime(2023, 1, 1, 10, 0, 0))

@pytest.fixture
def monthly_habit():
    return Habit("Monthly Report", "Write monthly report", "monthly", datetime(2023, 1, 1, 10, 0, 0))

@pytest.fixture
def quarterly_habit():
    return Habit("Quarterly Review", "Review quarterly goals", "quarterly", datetime(2023, 1, 1, 10, 0, 0))

@pytest.fixture
def annually_habit():
    return Habit("Annual Planning", "Plan for the next year", "annually", datetime(2023, 1, 1, 10, 0, 0))

def test_habit_initialization(daily_habit):
    assert daily_habit.name == "Daily Read"
    assert daily_habit.task_description == "Read a book daily"
    assert daily_habit.period == "daily"
    assert daily_habit.creation_time == datetime(2023, 1, 1, 10, 0, 0)

def test_habit_initialization_default_creation_time():
    habit = Habit("New Habit", "Description", "daily")
    assert isinstance(habit.creation_time, datetime)

def test_habit_unsupported_period():
    with pytest.raises(AssertionError, match="Unsupported period type provided."):
        Habit("Bad Habit", "Something", "fortnightly")

def test_habit_get_period_start_end_daily(daily_habit):
    target_time = datetime(2023, 1, 15, 14, 30, 0)
    start, end = daily_habit.get_period_start_end(target_time)
    assert start == datetime(2023, 1, 15, 0, 0, 0)
    assert end == datetime(2023, 1, 16, 0, 0, 0)

def test_habit_get_period_start_end_weekly(weekly_habit):
    target_time = datetime(2023, 1, 15, 14, 30, 0) # A Monday
    start, end = weekly_habit.get_period_start_end(target_time)
    assert start == datetime(2023, 1, 9, 0, 0, 0) # Monday of that week (assuming week starts on Monday)
    assert end == datetime(2023, 1, 16, 0, 0, 0) # Following Monday

def test_habit_get_period_start_end_monthly(monthly_habit):
    target_time = datetime(2023, 2, 15, 14, 30, 0)
    start, end = monthly_habit.get_period_start_end(target_time)
    assert start == datetime(2023, 2, 1, 0, 0, 0)
    assert end == datetime(2023, 3, 1, 0, 0, 0)

def test_habit_get_period_start_end_monthly_december(monthly_habit):
    target_time = datetime(2023, 12, 15, 14, 30, 0)
    start, end = monthly_habit.get_period_start_end(target_time)
    assert start == datetime(2023, 12, 1, 0, 0, 0)
    assert end == datetime(2024, 1, 1, 0, 0, 0)

def test_habit_get_period_start_end_quarterly(quarterly_habit):
    target_time = datetime(2023, 5, 15, 14, 30, 0) # May is in Q2 (April, May, June)
    start, end = quarterly_habit.get_period_start_end(target_time)
    assert start == datetime(2023, 4, 1, 0, 0, 0)
    assert end == datetime(2023, 7, 1, 0, 0, 0)

def test_habit_get_period_start_end_quarterly_q4(quarterly_habit):
    target_time = datetime(2023, 11, 15, 14, 30, 0) # Nov is in Q4 (Oct, Nov, Dec)
    start, end = quarterly_habit.get_period_start_end(target_time)
    assert start == datetime(2023, 10, 1, 0, 0, 0)
    assert end == datetime(2024, 1, 1, 0, 0, 0)

def test_habit_get_period_start_end_annually(annually_habit):
    target_time = datetime(2023, 7, 15, 14, 30, 0)
    start, end = annually_habit.get_period_start_end(target_time)
    assert start == datetime(2023, 1, 1, 0, 0, 0)
    assert end == datetime(2024, 1, 1, 0, 0, 0)

def test_habit_get_next_period_daily(daily_habit):
    period_end = datetime(2023, 1, 16, 0, 0, 0)
    next_start, next_end = daily_habit.get_next_period(period_end)
    assert next_start == datetime(2023, 1, 16, 0, 0, 0)
    assert next_end == datetime(2023, 1, 17, 0, 0, 0)

def test_habit_get_next_period_weekly(weekly_habit):
    period_end = datetime(2023, 1, 16, 0, 0, 0)
    next_start, next_end = weekly_habit.get_next_period(period_end)
    assert next_start == datetime(2023, 1, 16, 0, 0, 0)
    assert next_end == datetime(2023, 1, 23, 0, 0, 0)

def test_habit_get_next_period_monthly(monthly_habit):
    period_end = datetime(2023, 2, 1, 0, 0, 0)
    next_start, next_end = monthly_habit.get_next_period(period_end)
    assert next_start == datetime(2023, 2, 1, 0, 0, 0)
    assert next_end == datetime(2023, 3, 1, 0, 0, 0)

def test_habit_get_next_period_monthly_december(monthly_habit):
    period_end = datetime(2023, 12, 1, 0, 0, 0)
    next_start, next_end = monthly_habit.get_next_period(period_end)
    assert next_start == datetime(2023, 12, 1, 0, 0, 0)
    assert next_end == datetime(2024, 1, 1, 0, 0, 0)

def test_habit_get_next_period_quarterly(quarterly_habit):
    period_end = datetime(2023, 7, 1, 0, 0, 0) # End of Q2
    next_start, next_end = quarterly_habit.get_next_period(period_end)
    assert next_start == datetime(2023, 7, 1, 0, 0, 0)
    assert next_end == datetime(2023, 10, 1, 0, 0, 0)

def test_habit_get_next_period_quarterly_q4(quarterly_habit):
    period_end = datetime(2023, 10, 1, 0, 0, 0) # End of Q4
    next_start, next_end = quarterly_habit.get_next_period(period_end)
    assert next_start == datetime(2023, 10, 1, 0, 0, 0)
    assert next_end == datetime(2024, 1, 1, 0, 0, 0)

def test_habit_get_next_period_annually(annually_habit):
    period_end = datetime(2023, 1, 1, 0, 0, 0)
    next_start, next_end = annually_habit.get_next_period(period_end)
    assert next_start == datetime(2023, 1, 1, 0, 0, 0)
    assert next_end == datetime(2024, 1, 1, 0, 0, 0)

@patch('src.habit_tracking.habits.datetime')
def test_habit_get_all_periods_since_daily(mock_datetime, daily_habit):
    mock_datetime.now.return_value = datetime(2023, 1, 5, 12, 0, 0)
    mock_datetime.fromisoformat = datetime.fromisoformat # Keep original for parsing ISO strings
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow normal datetime object creation

    periods = daily_habit.get_all_periods_since(datetime(2023, 1, 3, 8, 0, 0))
    expected_periods = [
        (datetime(2023, 1, 3, 0, 0, 0), datetime(2023, 1, 4, 0, 0, 0)),
        (datetime(2023, 1, 4, 0, 0, 0), datetime(2023, 1, 5, 0, 0, 0))
    ]
    assert periods == expected_periods

@patch('src.habit_tracking.habits.datetime')
def test_habit_get_all_periods_since_weekly(mock_datetime, weekly_habit):
    mock_datetime.now.return_value = datetime(2023, 1, 20, 12, 0, 0) # Friday
    mock_datetime.fromisoformat = datetime.fromisoformat
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

    periods = weekly_habit.get_all_periods_since(datetime(2023, 1, 10, 8, 0, 0)) # Tuesday
    # Week 1: Mon 1/9 -> Mon 1/16
    # Week 2: Mon 1/16 -> Mon 1/23
    expected_periods = [
        (datetime(2023, 1, 9, 0, 0, 0), datetime(2023, 1, 16, 0, 0, 0))
    ]
    assert periods == expected_periods

def test_habit_json_representation(daily_habit):
    expected_json = {
        'name': "Daily Read",
        'task_description': "Read a book daily",
        'period': "daily",
        'creation_time': "2023-01-01T10:00:00"
    }
    assert daily_habit.json() == expected_json

# Tests for UserHabit
@pytest.fixture
def user_habit(daily_habit):
    return UserHabit(daily_habit, userhabit_id="uh1", completion_times=[], creation_time=datetime(2023, 1, 15))

def test_user_habit_initialization(user_habit, daily_habit):
    assert user_habit.habit == daily_habit
    assert user_habit.userhabit_id == "uh1"
    assert user_habit.completion_times == []
    assert user_habit.creation_time == datetime(2023, 1, 15)

def test_user_habit_initialization_default_id_and_times(daily_habit):
    uh = UserHabit(daily_habit)
    assert isinstance(uh.userhabit_id, str)
    assert len(uh.userhabit_id) > 0
    assert uh.completion_times == []
    assert isinstance(uh.creation_time, datetime)

def test_user_habit_period_completed_true(user_habit):
    user_habit.completion_times.append(datetime(2023, 1, 15, 12, 0, 0))
    period_start = datetime(2023, 1, 15, 0, 0, 0)
    period_end = datetime(2023, 1, 16, 0, 0, 0)
    assert user_habit.period_completed(period_start, period_end) is True

def test_user_habit_period_completed_false(user_habit):
    user_habit.completion_times.append(datetime(2023, 1, 14, 12, 0, 0))
    period_start = datetime(2023, 1, 15, 0, 0, 0)
    period_end = datetime(2023, 1, 16, 0, 0, 0)
    assert user_habit.period_completed(period_start, period_end) is False

@patch('src.habit_tracking.habits.datetime')
def test_user_habit_track_completion_success(mock_datetime, user_habit):
    mock_datetime.now.return_value = datetime(2023, 1, 15, 18, 0, 0)
    mock_datetime.fromisoformat = datetime.fromisoformat
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

    assert user_habit.track_completion() is True
    assert len(user_habit.completion_times) == 1
    assert user_habit.completion_times[0] == datetime(2023, 1, 15, 18, 0, 0)

@patch('src.habit_tracking.habits.datetime')
def test_user_habit_track_completion_already_completed(mock_datetime, user_habit):
    mock_datetime.now.return_value = datetime(2023, 1, 15, 18, 0, 0)
    mock_datetime.fromisoformat = datetime.fromisoformat
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
    user_habit.track_completion() # First completion
    assert user_habit.track_completion() is False # Attempt second completion in same period
    assert len(user_habit.completion_times) == 1 # Should not add another completion

@patch('src.habit_tracking.habits.datetime')
def test_user_habit_get_completion_history(mock_datetime, daily_habit):
    mock_datetime.now.return_value = datetime(2023, 1, 5, 12, 0, 0)
    mock_datetime.fromisoformat = datetime.fromisoformat
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

    uh = UserHabit(daily_habit, userhabit_id="uh_hist", creation_time=datetime(2023, 1, 3, 8, 0, 0))
    uh.completion_times.append(datetime(2023, 1, 3, 10, 0, 0)) # Completed on 1/3

    history = uh.get_completion_history()
    expected_history = [
        (datetime(2023, 1, 3, 0, 0, 0), datetime(2023, 1, 4, 0, 0, 0), True),
        (datetime(2023, 1, 4, 0, 0, 0), datetime(2023, 1, 5, 0, 0, 0), False)
    ]
    assert history == expected_history

def test_user_habit_json_representation(user_habit, daily_habit):
    user_habit.completion_times.append(datetime(2023, 1, 15, 12, 0, 0))
    expected_json = {
        "habit": daily_habit.name,
        "userhabit_id": "uh1",
        "completion_times": ["2023-01-15T12:00:00"],
        "creation_time": "2023-01-15T00:00:00"
    }
    assert user_habit.json() == expected_json


