import pytest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch

# Add src to path for importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from habit_tracking.habits import Habit, UserHabit


class TestHabit:
    """Test cases for the Habit class."""

    def test_habit_creation_with_defaults(self):
        """Test creating a habit with default creation time."""
        name = "Test Habit"
        description = "Test description"
        period = "daily"
        
        habit = Habit(name, description, period)
        
        assert habit.name == name
        assert habit.task_description == description
        assert habit.period == period
        assert isinstance(habit.creation_time, datetime)
        # Creation time should be close to now (within 1 second)
        assert abs((datetime.now() - habit.creation_time).total_seconds()) < 1

    def test_habit_creation_with_custom_time(self):
        """Test creating a habit with custom creation time."""
        name = "Test Habit"
        description = "Test description"
        period = "weekly"
        creation_time = datetime(2023, 1, 1, 12, 0, 0)
        
        habit = Habit(name, description, period, creation_time)
        
        assert habit.name == name
        assert habit.task_description == description
        assert habit.period == period
        assert habit.creation_time == creation_time

    def test_valid_periods(self):
        """Test that all valid periods are accepted."""
        valid_periods = ['daily', 'weekly', 'monthly', 'quarterly', 'annually']
        
        for period in valid_periods:
            habit = Habit("Test", "Description", period)
            assert habit.period == period

    def test_invalid_period_raises_assertion_error(self):
        """Test that invalid periods raise AssertionError."""
        invalid_periods = ['hourly', 'biweekly', 'yearly', 'invalid']
        
        for period in invalid_periods:
            with pytest.raises(AssertionError, match="Unsupported period type provided"):
                Habit("Test", "Description", period)

    def test_get_period_start_end_daily(self):
        """Test period calculation for daily habits."""
        habit = Habit("Test", "Description", "daily")
        target_time = datetime(2023, 5, 15, 14, 30, 0)
        
        start, end = habit.get_period_start_end(target_time)
        
        assert start == datetime(2023, 5, 15, 0, 0, 0)
        assert end == datetime(2023, 5, 16, 0, 0, 0)

    def test_get_period_start_end_weekly(self):
        """Test period calculation for weekly habits."""
        habit = Habit("Test", "Description", "weekly")
        # Monday 2023-05-15
        target_time = datetime(2023, 5, 15, 14, 30, 0)
        
        start, end = habit.get_period_start_end(target_time)
        
        # Should start on Monday (preserving time) and end next Monday
        assert start == datetime(2023, 5, 15, 14, 30, 0)
        assert end == datetime(2023, 5, 22, 14, 30, 0)

    def test_get_period_start_end_monthly(self):
        """Test period calculation for monthly habits."""
        habit = Habit("Test", "Description", "monthly")
        target_time = datetime(2023, 5, 15, 14, 30, 0)
        
        start, end = habit.get_period_start_end(target_time)
        
        assert start == datetime(2023, 5, 1, 0, 0, 0)
        assert end == datetime(2023, 6, 1, 0, 0, 0)

    def test_get_period_start_end_monthly_december(self):
        """Test period calculation for monthly habits in December."""
        habit = Habit("Test", "Description", "monthly")
        target_time = datetime(2023, 12, 15, 14, 30, 0)
        
        start, end = habit.get_period_start_end(target_time)
        
        assert start == datetime(2023, 12, 1, 0, 0, 0)
        assert end == datetime(2024, 1, 1, 0, 0, 0)

    def test_get_period_start_end_quarterly(self):
        """Test period calculation for quarterly habits."""
        habit = Habit("Test", "Description", "quarterly")
        
        # Test Q1 (January)
        target_time = datetime(2023, 2, 15, 14, 30, 0)
        start, end = habit.get_period_start_end(target_time)
        assert start == datetime(2023, 1, 1, 0, 0, 0)
        assert end == datetime(2023, 4, 1, 0, 0, 0)
        
        # Test Q2 (April)
        target_time = datetime(2023, 5, 15, 14, 30, 0)
        start, end = habit.get_period_start_end(target_time)
        assert start == datetime(2023, 4, 1, 0, 0, 0)
        assert end == datetime(2023, 7, 1, 0, 0, 0)
        
        # Test Q3 (July)
        target_time = datetime(2023, 8, 15, 14, 30, 0)
        start, end = habit.get_period_start_end(target_time)
        assert start == datetime(2023, 7, 1, 0, 0, 0)
        assert end == datetime(2023, 10, 1, 0, 0, 0)
        
        # Test Q4 (October)
        target_time = datetime(2023, 11, 15, 14, 30, 0)
        start, end = habit.get_period_start_end(target_time)
        assert start == datetime(2023, 10, 1, 0, 0, 0)
        assert end == datetime(2024, 1, 1, 0, 0, 0)

    def test_get_period_start_end_annually(self):
        """Test period calculation for annual habits."""
        habit = Habit("Test", "Description", "annually")
        target_time = datetime(2023, 5, 15, 14, 30, 0)
        
        start, end = habit.get_period_start_end(target_time)
        
        assert start == datetime(2023, 1, 1, 0, 0, 0)
        assert end == datetime(2024, 1, 1, 0, 0, 0)

    def test_get_next_period_daily(self):
        """Test next period calculation for daily habits."""
        habit = Habit("Test", "Description", "daily")
        period_end = datetime(2023, 5, 16, 0, 0, 0)
        
        next_start, next_end = habit.get_next_period(period_end)
        
        assert next_start == datetime(2023, 5, 16, 0, 0, 0)
        assert next_end == datetime(2023, 5, 17, 0, 0, 0)

    def test_get_next_period_weekly(self):
        """Test next period calculation for weekly habits."""
        habit = Habit("Test", "Description", "weekly")
        period_end = datetime(2023, 5, 22, 0, 0, 0)
        
        next_start, next_end = habit.get_next_period(period_end)
        
        assert next_start == datetime(2023, 5, 22, 0, 0, 0)
        assert next_end == datetime(2023, 5, 29, 0, 0, 0)

    def test_get_next_period_monthly(self):
        """Test next period calculation for monthly habits."""
        habit = Habit("Test", "Description", "monthly")
        period_end = datetime(2023, 6, 1, 0, 0, 0)
        
        next_start, next_end = habit.get_next_period(period_end)
        
        assert next_start == datetime(2023, 6, 1, 0, 0, 0)
        assert next_end == datetime(2023, 7, 1, 0, 0, 0)

    def test_get_all_periods_since(self):
        """Test getting all periods since a start time."""
        habit = Habit("Test", "Description", "daily")
        start_time = datetime(2023, 5, 15, 0, 0, 0)
        
        # Mock datetime.now() to return a specific time
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 18, 0, 0, 0)
            # Mock the datetime constructor to behave normally
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            periods = habit.get_all_periods_since(start_time)
            
            expected_periods = [
                (datetime(2023, 5, 15, 0, 0, 0), datetime(2023, 5, 16, 0, 0, 0)),
                (datetime(2023, 5, 16, 0, 0, 0), datetime(2023, 5, 17, 0, 0, 0)),
                (datetime(2023, 5, 17, 0, 0, 0), datetime(2023, 5, 18, 0, 0, 0))
            ]
            
            assert periods == expected_periods

    def test_json_serialization(self):
        """Test JSON serialization of Habit objects."""
        creation_time = datetime(2023, 5, 15, 12, 30, 0)
        habit = Habit("Test Habit", "Test description", "daily", creation_time)
        
        json_data = habit.json()
        
        expected = {
            'name': 'Test Habit',
            'task_description': 'Test description',
            'period': 'daily',
            'creation_time': '2023-05-15T12:30:00'
        }
        
        assert json_data == expected


class TestUserHabit:
    """Test cases for the UserHabit class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.habit = Habit("Test Habit", "Test description", "daily")

    def test_user_habit_creation_with_defaults(self):
        """Test creating a UserHabit with default values."""
        user_habit = UserHabit(self.habit)
        
        assert user_habit.habit == self.habit
        assert len(user_habit.userhabit_id) == 32  # UUID hex string length
        assert user_habit.completion_times == []
        assert isinstance(user_habit.creation_time, datetime)
        # Creation time should be close to now (within 1 second)
        assert abs((datetime.now() - user_habit.creation_time).total_seconds()) < 1

    def test_user_habit_creation_with_custom_values(self):
        """Test creating a UserHabit with custom values."""
        userhabit_id = "custom_id"
        completion_times = [datetime(2023, 5, 15, 12, 0, 0)]
        creation_time = datetime(2023, 5, 1, 10, 0, 0)
        
        user_habit = UserHabit(
            self.habit, 
            userhabit_id=userhabit_id,
            completion_times=completion_times,
            creation_time=creation_time
        )
        
        assert user_habit.habit == self.habit
        assert user_habit.userhabit_id == userhabit_id
        assert user_habit.completion_times == completion_times
        assert user_habit.creation_time == creation_time

    def test_period_completed_true(self):
        """Test period_completed returns True when habit was completed in period."""
        completion_time = datetime(2023, 5, 15, 12, 0, 0)
        user_habit = UserHabit(self.habit, completion_times=[completion_time])
        
        period_start = datetime(2023, 5, 15, 0, 0, 0)
        period_end = datetime(2023, 5, 16, 0, 0, 0)
        
        assert user_habit.period_completed(period_start, period_end) is True

    def test_period_completed_false(self):
        """Test period_completed returns False when habit was not completed in period."""
        completion_time = datetime(2023, 5, 14, 12, 0, 0)  # Before period
        user_habit = UserHabit(self.habit, completion_times=[completion_time])
        
        period_start = datetime(2023, 5, 15, 0, 0, 0)
        period_end = datetime(2023, 5, 16, 0, 0, 0)
        
        assert user_habit.period_completed(period_start, period_end) is False

    def test_period_completed_edge_cases(self):
        """Test period_completed edge cases (exact boundaries)."""
        user_habit = UserHabit(self.habit)
        
        # Completion exactly at period start
        completion_time = datetime(2023, 5, 15, 0, 0, 0)
        user_habit.completion_times = [completion_time]
        period_start = datetime(2023, 5, 15, 0, 0, 0)
        period_end = datetime(2023, 5, 16, 0, 0, 0)
        assert user_habit.period_completed(period_start, period_end) is True
        
        # Completion exactly at period end (should be False - end is exclusive)
        completion_time = datetime(2023, 5, 16, 0, 0, 0)
        user_habit.completion_times = [completion_time]
        assert user_habit.period_completed(period_start, period_end) is False

    def test_track_completion_success(self):
        """Test successful tracking of habit completion."""
        user_habit = UserHabit(self.habit)
        completion_time = datetime(2023, 5, 15, 12, 0, 0)
        
        result = user_habit.track_completion(completion_time)
        
        assert result is True
        assert completion_time in user_habit.completion_times
        assert len(user_habit.completion_times) == 1

    def test_track_completion_default_time(self):
        """Test tracking completion with default time (now)."""
        user_habit = UserHabit(self.habit)
        
        result = user_habit.track_completion()
        
        assert result is True
        assert len(user_habit.completion_times) == 1
        # Should be close to current time
        completion_time = user_habit.completion_times[0]
        assert abs((datetime.now() - completion_time).total_seconds()) < 1

    def test_track_completion_already_completed(self):
        """Test tracking completion when already completed in same period."""
        completion_time = datetime(2023, 5, 15, 12, 0, 0)
        user_habit = UserHabit(self.habit, completion_times=[completion_time])
        
        # Try to complete again in same period
        new_completion_time = datetime(2023, 5, 15, 18, 0, 0)
        result = user_habit.track_completion(new_completion_time)
        
        assert result is False
        assert len(user_habit.completion_times) == 1  # No new completion added
        assert new_completion_time not in user_habit.completion_times

    def test_get_completion_history(self):
        """Test getting completion history for a habit."""
        creation_time = datetime(2023, 5, 1, 0, 0, 0)
        user_habit = UserHabit(self.habit, creation_time=creation_time)
        
        # Add some completions
        user_habit.completion_times = [
            datetime(2023, 5, 1, 12, 0, 0),
            datetime(2023, 5, 3, 12, 0, 0)
        ]
        
        # Mock datetime.now() to return a specific time
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 5, 0, 0, 0)
            # Mock the datetime constructor to behave normally
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            history = user_habit.get_completion_history()
            
            # Should have 4 days: May 1-4 (May 5 is current day, not completed yet)
            assert len(history) == 4
            
            # Check first day (completed)
            start, end, completed = history[0]
            assert start == datetime(2023, 5, 1, 0, 0, 0)
            assert end == datetime(2023, 5, 2, 0, 0, 0)
            assert completed is True
            
            # Check second day (not completed)
            start, end, completed = history[1]
            assert start == datetime(2023, 5, 2, 0, 0, 0)
            assert end == datetime(2023, 5, 3, 0, 0, 0)
            assert completed is False
            
            # Check third day (completed)
            start, end, completed = history[2]
            assert start == datetime(2023, 5, 3, 0, 0, 0)
            assert end == datetime(2023, 5, 4, 0, 0, 0)
            assert completed is True

    def test_json_serialization(self):
        """Test JSON serialization of UserHabit objects."""
        creation_time = datetime(2023, 5, 1, 12, 0, 0)
        completion_times = [datetime(2023, 5, 1, 18, 0, 0)]
        user_habit = UserHabit(
            self.habit,
            userhabit_id="test_id",
            completion_times=completion_times,
            creation_time=creation_time
        )
        
        json_data = user_habit.json()
        
        expected = {
            "habit": "Test Habit",
            "userhabit_id": "test_id",
            "completion_times": ["2023-05-01T18:00:00"],
            "creation_time": "2023-05-01T12:00:00"
        }
        
        assert json_data == expected


if __name__ == '__main__':
    pytest.main([__file__])