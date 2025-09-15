"""
Tests for the demo data creation script.
"""

import os
import sys
import tempfile
import pytest
from datetime import datetime, timedelta

# Get the absolute path of the src directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)

# Import the script functions
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from create_demo_data import (
    create_realistic_habits,
    create_demo_users_with_habits,
    save_demo_data,
    generate_completion_data
)
from data_storage.json import JsonStorageInterface
from habit_tracking.habits import Habit, UserHabit


class TestDemoDataCreation:
    """Test the demo data creation functionality."""

    def test_create_realistic_habits(self):
        """Test that realistic habits are created correctly."""
        habits = create_realistic_habits()
        
        # Check that we have the expected number of habits
        assert len(habits) == 24
        
        # Check that all habits are valid Habit objects
        for habit in habits:
            assert isinstance(habit, Habit)
            assert len(habit.name) > 0
            assert len(habit.task_description) > 0
            assert habit.period in ['daily', 'weekly', 'monthly', 'quarterly', 'annually']
            assert isinstance(habit.creation_time, datetime)
        
        # Check that we have habits for each periodicity
        periods = [habit.period for habit in habits]
        assert 'daily' in periods
        assert 'weekly' in periods
        assert 'monthly' in periods
        assert 'quarterly' in periods
        assert 'annually' in periods
        
        # Check that habit names are unique
        names = [habit.name for habit in habits]
        assert len(names) == len(set(names))

    def test_create_demo_users_with_habits(self):
        """Test that demo users are created correctly."""
        habits = create_realistic_habits()
        users = create_demo_users_with_habits(habits, days_of_data=30)
        
        # Check that we have the expected number of users
        assert len(users) == 5
        
        # Check that all users have unique usernames
        usernames = [user.username for user in users]
        assert len(usernames) == len(set(usernames))
        
        # Check that all users have habits
        for user in users:
            assert len(user.habits) > 0
            assert len(user.habits) <= len(habits)
            
            # Check that each user habit is valid
            for user_habit in user.habits:
                assert isinstance(user_habit, UserHabit)
                assert isinstance(user_habit.habit, Habit)
                assert len(user_habit.completion_times) >= 0

    def test_completion_data_generation(self):
        """Test that completion data is generated realistically."""
        # Create habit with creation time in the past
        creation_time = datetime.now() - timedelta(days=35)
        habit = Habit("Test Habit", "Test description", "daily", creation_time=creation_time)
        user_habit = UserHabit(habit=habit, creation_time=creation_time)
        
        # Generate completion data for 30 days
        generate_completion_data(user_habit, 30, 0.8)
        
        # Check that we have some completions
        assert len(user_habit.completion_times) > 0
        
        # Check that completion times are within the expected range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        for completion_time in user_habit.completion_times:
            assert isinstance(completion_time, datetime)
            assert start_date <= completion_time <= end_date

    def test_save_demo_data(self):
        """Test that demo data can be saved and loaded correctly."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        try:
            # Create sample data
            habits = create_realistic_habits()[:5]  # Use fewer habits for test
            users = create_demo_users_with_habits(habits, days_of_data=10)[:2]  # Use fewer users
            
            # Save the data
            save_demo_data(users, habits, temp_path)
            
            # Check that file was created
            assert os.path.exists(temp_path)
            
            # Load data back and verify
            storage = JsonStorageInterface(temp_path)
            
            # Check that all habits were saved
            saved_habits = storage.get_all_habits()
            assert len(saved_habits) == len(habits)
            
            # Check that all users were saved
            for user in users:
                saved_user = storage.get_user(user.username)
                assert saved_user is not None
                assert saved_user.username == user.username
                assert len(saved_user.habits) == len(user.habits)
                
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_data_coverage_requirements(self):
        """Test that the generated data meets the 30-day coverage requirement."""
        habits = create_realistic_habits()
        users = create_demo_users_with_habits(habits, days_of_data=30)
        
        # Check that we have data spanning at least 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        total_completions = 0
        for user in users:
            for user_habit in user.habits:
                for completion_time in user_habit.completion_times:
                    if start_date <= completion_time <= end_date:
                        total_completions += 1
        
        # We should have a substantial number of completions over 30 days
        assert total_completions >= 100, f"Expected at least 100 completions, got {total_completions}"

    def test_realistic_completion_patterns(self):
        """Test that completion patterns are realistic."""
        habits = create_realistic_habits()
        users = create_demo_users_with_habits(habits, days_of_data=30)
        
        # Check that daily habits have more completions than quarterly/annual habits
        daily_completions = []
        quarterly_completions = []
        
        for user in users:
            for user_habit in user.habits:
                completion_count = len(user_habit.completion_times)
                if user_habit.habit.period == 'daily':
                    daily_completions.append(completion_count)
                elif user_habit.habit.period == 'quarterly':
                    quarterly_completions.append(completion_count)
        
        if daily_completions and quarterly_completions:
            avg_daily = sum(daily_completions) / len(daily_completions)
            avg_quarterly = sum(quarterly_completions) / len(quarterly_completions)
            
            # Daily habits should have more completions on average
            assert avg_daily > avg_quarterly