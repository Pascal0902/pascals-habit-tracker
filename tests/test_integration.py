import pytest
import sys
import os
import tempfile
from datetime import datetime

# Add src to path for importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_storage.json import JsonStorageInterface
from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User
from habit_analysis.analytics import (
    get_all_tracked_habits_with_streak,
    get_current_longest_habit_streak
)


class TestIntegration:
    """Integration tests to verify modules work together correctly."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        # Write initial empty JSON structure
        import json
        json.dump({"users": {}, "habits": {}, "user_habits": {}}, self.temp_file)
        self.temp_file.close()
        self.storage = JsonStorageInterface(self.temp_file.name)

    def teardown_method(self):
        """Clean up test fixtures."""
        try:
            os.unlink(self.temp_file.name)
        except FileNotFoundError:
            pass

    def test_complete_habit_tracking_workflow(self):
        """Test a complete workflow from habit creation to analysis."""
        # 1. Create habits
        exercise_habit = Habit("Exercise", "Daily workout", "daily")
        reading_habit = Habit("Reading", "Read for 30 minutes", "weekly")
        
        # 2. Store habits
        assert self.storage.insert_habit(exercise_habit)
        assert self.storage.insert_habit(reading_habit)
        
        # 3. Create user
        user = User("testuser")
        assert self.storage.insert_user(user)
        
        # 4. User adds habits to tracking with specific creation time
        creation_time = datetime(2023, 5, 1, 0, 0, 0)
        exercise_user_habit = UserHabit(exercise_habit, creation_time=creation_time)
        reading_user_habit = UserHabit(reading_habit, creation_time=creation_time)
        user.habits = [exercise_user_habit, reading_user_habit]
        
        # 5. Store user habits
        assert self.storage.insert_user_habit(exercise_user_habit)
        assert self.storage.insert_user_habit(reading_user_habit)
        
        # 6. Update user with habit references
        assert self.storage.update_user(user)
        
        # 7. Track some completions
        completion_dates = [
            datetime(2023, 5, 10, 12, 0, 0),
            datetime(2023, 5, 11, 12, 0, 0),
            datetime(2023, 5, 12, 12, 0, 0)
        ]
        
        for date in completion_dates:
            success = exercise_user_habit.track_completion(date)
            assert success is True
        
        # Track reading completion
        reading_completion = datetime(2023, 5, 8, 14, 0, 0)
        success = reading_user_habit.track_completion(reading_completion)
        assert success is True
        
        # 8. Update stored user habits
        assert self.storage.update_user_habit(exercise_user_habit)
        assert self.storage.update_user_habit(reading_user_habit)
        
        # 9. Retrieve user from storage
        retrieved_user = self.storage.get_user("testuser")
        assert retrieved_user is not None
        assert len(retrieved_user.habits) == 2
        
        # 10. Analyze habits
        from unittest.mock import patch
        with patch('habit_tracking.habits.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 13, 0, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            habits_with_streaks = get_all_tracked_habits_with_streak(retrieved_user)
            assert len(habits_with_streaks) == 2
            
            # Find exercise habit streak
            exercise_streak = None
            for habit, streak in habits_with_streaks:
                if habit.name == "Exercise":
                    exercise_streak = streak
                    break
            
            assert exercise_streak == 3  # 3 consecutive days
            
            # Get current longest streak
            longest_habit, longest_streak = get_current_longest_habit_streak(retrieved_user)
            assert longest_habit.name == "Exercise"
            assert longest_streak == 3

    def test_persistence_across_storage_instances(self):
        """Test that data persists across different storage instances."""
        # Create and store data with first instance
        habit = Habit("Test Habit", "Test description", "daily")
        user = User("testuser")
        
        self.storage.insert_habit(habit)
        self.storage.insert_user(user)
        
        user_habit = user.add_habit(habit)
        self.storage.insert_user_habit(user_habit)
        self.storage.update_user(user)
        
        # Create new storage instance with same file
        new_storage = JsonStorageInterface(self.temp_file.name)
        
        # Retrieve data with new instance
        retrieved_habit = new_storage.get_habit("Test Habit")
        retrieved_user = new_storage.get_user("testuser")
        
        assert retrieved_habit is not None
        assert retrieved_habit.name == "Test Habit"
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        assert len(retrieved_user.habits) == 1

    def test_habit_deletion_workflow(self):
        """Test deleting habits and cleaning up related data."""
        # Create and store habit
        habit = Habit("Temporary Habit", "Will be deleted", "daily")
        self.storage.insert_habit(habit)
        
        # Create user and add habit
        user = User("testuser")
        self.storage.insert_user(user)
        
        user_habit = user.add_habit(habit)
        self.storage.insert_user_habit(user_habit)
        self.storage.update_user(user)
        
        # Verify habit exists
        assert self.storage.get_habit("Temporary Habit") is not None
        assert len(self.storage.get_all_user_habits()) == 1
        
        # Delete user habit
        user.remove_habit(habit)
        self.storage.delete_user_habit(user_habit)
        self.storage.update_user(user)
        
        # Delete habit
        self.storage.delete_habit(habit)
        
        # Verify deletion
        assert self.storage.get_habit("Temporary Habit") is None
        assert len(self.storage.get_all_user_habits()) == 0
        
        retrieved_user = self.storage.get_user("testuser")
        assert len(retrieved_user.habits) == 0

    def test_multiple_users_same_habits(self):
        """Test multiple users tracking the same habits independently."""
        # Create shared habits
        habit1 = Habit("Exercise", "Daily workout", "daily")
        habit2 = Habit("Reading", "Read books", "weekly")
        
        self.storage.insert_habit(habit1)
        self.storage.insert_habit(habit2)
        
        # Create two users
        user1 = User("user1")
        user2 = User("user2")
        
        self.storage.insert_user(user1)
        self.storage.insert_user(user2)
        
        # Both users add the same habits
        user1_habit1 = user1.add_habit(habit1)
        user1_habit2 = user1.add_habit(habit2)
        user2_habit1 = user2.add_habit(habit1)
        user2_habit2 = user2.add_habit(habit2)
        
        # Store user habits
        self.storage.insert_user_habit(user1_habit1)
        self.storage.insert_user_habit(user1_habit2)
        self.storage.insert_user_habit(user2_habit1)
        self.storage.insert_user_habit(user2_habit2)
        
        # Update users
        self.storage.update_user(user1)
        self.storage.update_user(user2)
        
        # Track different completions for each user
        completion_time = datetime(2023, 5, 15, 12, 0, 0)
        user1_habit1.track_completion(completion_time)
        # user2 doesn't complete anything
        
        self.storage.update_user_habit(user1_habit1)
        
        # Retrieve and verify independence
        retrieved_user1 = self.storage.get_user("user1")
        retrieved_user2 = self.storage.get_user("user2")
        
        assert len(retrieved_user1.habits) == 2
        assert len(retrieved_user2.habits) == 2
        
        # Check completion independence
        user1_exercise = None
        user2_exercise = None
        
        for uh in retrieved_user1.habits:
            if uh.habit.name == "Exercise":
                user1_exercise = uh
                break
                
        for uh in retrieved_user2.habits:
            if uh.habit.name == "Exercise":
                user2_exercise = uh
                break
        
        assert len(user1_exercise.completion_times) == 1
        assert len(user2_exercise.completion_times) == 0


if __name__ == '__main__':
    pytest.main([__file__])