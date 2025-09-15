import pytest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch

# Add src to path for importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from habit_analysis.analytics import (
    get_all_tracked_habits_with_streak,
    get_all_tracked_habits_with_streak_for_periodicity,
    get_all_time_longest_habit_streak,
    get_current_longest_habit_streak,
    get_longest_streak_for_habit,
    get_current_streak_for_habit
)
from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


class TestAnalytics:
    """Test cases for habit analysis functions."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create habits with different periods
        self.daily_habit = Habit("Exercise", "Daily workout", "daily")
        self.weekly_habit = Habit("Reading", "Read a book", "weekly")
        self.monthly_habit = Habit("Review", "Monthly review", "monthly")
        
        # Create user
        self.user = User("testuser")

    def create_user_habit_with_completions(self, habit, completion_dates):
        """Helper to create UserHabit with specific completion dates."""
        user_habit = UserHabit(habit, creation_time=datetime(2023, 1, 1, 0, 0, 0))
        user_habit.completion_times = [
            datetime.fromisoformat(date) if isinstance(date, str) else date
            for date in completion_dates
        ]
        return user_habit

    def test_get_all_tracked_habits_with_streak_empty_user(self):
        """Test getting streaks when user has no habits."""
        result = get_all_tracked_habits_with_streak(self.user)
        assert result == []

    def test_get_all_tracked_habits_with_streak_no_completions(self):
        """Test getting streaks when habits have no completions."""
        # Create user habits with creation time before the mocked 'now'
        user_habit1 = UserHabit(self.daily_habit, creation_time=datetime(2023, 5, 1, 0, 0, 0))
        user_habit2 = UserHabit(self.weekly_habit, creation_time=datetime(2023, 5, 1, 0, 0, 0))
        self.user.habits = [user_habit1, user_habit2]
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_all_tracked_habits_with_streak(self.user)
            
            assert len(result) == 2
            for habit, streak in result:
                assert streak == 0

    def test_get_all_tracked_habits_with_streak_perfect_streak(self):
        """Test getting streaks with perfect completion history."""
        # Create daily habit with 5 consecutive days completed
        completion_dates = [
            "2023-05-10T12:00:00",
            "2023-05-11T12:00:00", 
            "2023-05-12T12:00:00",
            "2023-05-13T12:00:00",
            "2023-05-14T12:00:00"
        ]
        user_habit = self.create_user_habit_with_completions(self.daily_habit, completion_dates)
        self.user.habits = [user_habit]
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_all_tracked_habits_with_streak(self.user)
            
            assert len(result) == 1
            habit, streak = result[0]
            assert habit.name == "Exercise"
            assert streak == 5

    def test_get_all_tracked_habits_with_streak_broken_streak(self):
        """Test getting streaks with broken completion history."""
        # Create habit with gap in completions
        completion_dates = [
            "2023-05-10T12:00:00",
            "2023-05-11T12:00:00",
            # Gap on 2023-05-12
            "2023-05-13T12:00:00",
            "2023-05-14T12:00:00"
        ]
        user_habit = self.create_user_habit_with_completions(self.daily_habit, completion_dates)
        self.user.habits = [user_habit]
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_all_tracked_habits_with_streak(self.user)
            
            assert len(result) == 1
            habit, streak = result[0]
            assert habit.name == "Exercise"
            assert streak == 2  # Only the last 2 consecutive days

    def test_get_all_tracked_habits_with_streak_current_period_incomplete(self):
        """Test that current incomplete period is not counted in streak."""
        # Create habit completed until yesterday
        completion_dates = [
            "2023-05-13T12:00:00",
            "2023-05-14T12:00:00"
        ]
        user_habit = self.create_user_habit_with_completions(self.daily_habit, completion_dates)
        self.user.habits = [user_habit]
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 12, 0, 0)  # Current day
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_all_tracked_habits_with_streak(self.user)
            
            assert len(result) == 1
            habit, streak = result[0]
            assert streak == 2  # Should not count today since it's incomplete

    def test_get_all_tracked_habits_with_streak_for_periodicity(self):
        """Test getting streaks filtered by periodicity."""
        # Create habits with different periods
        daily_user_habit = self.create_user_habit_with_completions(
            self.daily_habit, ["2023-05-13T12:00:00", "2023-05-14T12:00:00"]
        )
        weekly_user_habit = self.create_user_habit_with_completions(
            self.weekly_habit, ["2023-05-01T12:00:00", "2023-05-08T12:00:00"]
        )
        monthly_user_habit = self.create_user_habit_with_completions(
            self.monthly_habit, ["2023-04-15T12:00:00"]
        )
        
        self.user.habits = [daily_user_habit, weekly_user_habit, monthly_user_habit]
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            # Test daily habits only
            result = get_all_tracked_habits_with_streak_for_periodicity(self.user, "daily")
            assert len(result) == 1
            assert result[0][0].name == "Exercise"
            
            # Test weekly habits only
            result = get_all_tracked_habits_with_streak_for_periodicity(self.user, "weekly")
            assert len(result) == 1
            assert result[0][0].name == "Reading"
            
            # Test monthly habits only
            result = get_all_tracked_habits_with_streak_for_periodicity(self.user, "monthly")
            assert len(result) == 1
            assert result[0][0].name == "Review"
            
            # Test non-existent periodicity
            result = get_all_tracked_habits_with_streak_for_periodicity(self.user, "quarterly")
            assert result == []

    def test_get_all_time_longest_habit_streak_single_habit(self):
        """Test getting all-time longest streak with single habit."""
        # Create habit with two separate streaks
        completion_dates = [
            "2023-05-01T12:00:00",
            "2023-05-02T12:00:00",
            "2023-05-03T12:00:00",  # Streak of 3
            # Gap
            "2023-05-10T12:00:00",
            "2023-05-11T12:00:00",
            "2023-05-12T12:00:00",
            "2023-05-13T12:00:00",
            "2023-05-14T12:00:00"   # Streak of 5
        ]
        user_habit = self.create_user_habit_with_completions(self.daily_habit, completion_dates)
        self.user.habits = [user_habit]
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_all_time_longest_habit_streak(self.user)
            
            habit, streak = result
            assert habit.name == "Exercise"
            assert streak == 5  # Longest streak

    def test_get_all_time_longest_habit_streak_multiple_habits(self):
        """Test getting all-time longest streak with multiple habits."""
        # Daily habit with streak of 3
        daily_completions = ["2023-05-01T12:00:00", "2023-05-02T12:00:00", "2023-05-03T12:00:00"]
        daily_user_habit = self.create_user_habit_with_completions(self.daily_habit, daily_completions)
        
        # Weekly habit with streak of 4
        weekly_completions = [
            "2023-04-03T12:00:00",
            "2023-04-10T12:00:00", 
            "2023-04-17T12:00:00",
            "2023-04-24T12:00:00"
        ]
        weekly_user_habit = self.create_user_habit_with_completions(self.weekly_habit, weekly_completions)
        
        self.user.habits = [daily_user_habit, weekly_user_habit]
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_all_time_longest_habit_streak(self.user)
            
            habit, streak = result
            assert habit.name == "Reading"  # Weekly habit has longer streak
            assert streak == 4

    def test_get_all_time_longest_habit_streak_no_habits(self):
        """Test getting all-time longest streak with no habits."""
        result = get_all_time_longest_habit_streak(self.user)
        
        habit, streak = result
        assert habit is None
        assert streak == 0

    def test_get_current_longest_habit_streak(self):
        """Test getting current longest streak."""
        # Create habits with different current streaks
        daily_completions = ["2023-05-13T12:00:00", "2023-05-14T12:00:00"]  # Current streak: 2
        daily_user_habit = self.create_user_habit_with_completions(self.daily_habit, daily_completions)
        
        weekly_completions = [
            "2023-04-24T12:00:00",
            "2023-05-01T12:00:00",
            "2023-05-08T12:00:00"  # Current streak: 3
        ]
        weekly_user_habit = self.create_user_habit_with_completions(self.weekly_habit, weekly_completions)
        
        self.user.habits = [daily_user_habit, weekly_user_habit]
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_current_longest_habit_streak(self.user)
            
            habit, streak = result
            assert habit.name == "Reading"  # Weekly habit has longer current streak
            assert streak == 3

    def test_get_longest_streak_for_habit(self):
        """Test getting longest streak for specific habit."""
        completion_dates = [
            "2023-05-01T12:00:00",
            "2023-05-02T12:00:00",  # Streak of 2
            # Gap
            "2023-05-10T12:00:00",
            "2023-05-11T12:00:00",
            "2023-05-12T12:00:00",
            "2023-05-13T12:00:00"   # Streak of 4
        ]
        user_habit = self.create_user_habit_with_completions(self.daily_habit, completion_dates)
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_longest_streak_for_habit(user_habit)
            
            assert result == 4

    def test_get_current_streak_for_habit(self):
        """Test getting current streak for specific habit."""
        completion_dates = [
            "2023-05-01T12:00:00",
            "2023-05-02T12:00:00",  # Old streak
            # Gap
            "2023-05-12T12:00:00",
            "2023-05-13T12:00:00",
            "2023-05-14T12:00:00"   # Current streak of 3
        ]
        user_habit = self.create_user_habit_with_completions(self.daily_habit, completion_dates)
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_current_streak_for_habit(user_habit)
            
            assert result == 3

    def test_get_current_streak_for_habit_no_completions(self):
        """Test getting current streak when habit has no completions."""
        user_habit = UserHabit(self.daily_habit, creation_time=datetime(2023, 5, 1, 0, 0, 0))
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_current_streak_for_habit(user_habit)
            
            assert result == 0

    def test_weekly_habit_streak_calculation(self):
        """Test streak calculation for weekly habits."""
        # Create weekly habit completed for 3 consecutive weeks
        completion_dates = [
            "2023-04-24T12:00:00",  # Week starting April 24
            "2023-05-01T12:00:00",  # Week starting May 1
            "2023-05-08T12:00:00"   # Week starting May 8
        ]
        user_habit = self.create_user_habit_with_completions(self.weekly_habit, completion_dates)
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)  # Monday of current week
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            current_streak = get_current_streak_for_habit(user_habit)
            longest_streak = get_longest_streak_for_habit(user_habit)
            
            assert current_streak == 3
            assert longest_streak == 3

    def test_monthly_habit_streak_calculation(self):
        """Test streak calculation for monthly habits."""
        # Create monthly habit completed for 3 consecutive months
        completion_dates = [
            "2023-03-15T12:00:00",  # March
            "2023-04-15T12:00:00",  # April
            "2023-05-01T12:00:00"   # May
        ]
        user_habit = self.create_user_habit_with_completions(self.monthly_habit, completion_dates)
        
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 15, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            current_streak = get_current_streak_for_habit(user_habit)
            longest_streak = get_longest_streak_for_habit(user_habit)
            
            assert current_streak == 3
            assert longest_streak == 3


if __name__ == '__main__':
    pytest.main([__file__])