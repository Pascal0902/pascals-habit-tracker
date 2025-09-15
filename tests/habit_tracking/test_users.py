import pytest
import sys
import os
from datetime import datetime

# Add src to path for importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


class TestUser:
    """Test cases for the User class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.habit1 = Habit("Exercise", "Go for a run", "daily")
        self.habit2 = Habit("Reading", "Read a book", "weekly")
        self.habit3 = Habit("Meditation", "Meditate for 10 minutes", "daily")

    def test_user_creation_with_defaults(self):
        """Test creating a user with default values."""
        username = "testuser"
        user = User(username)
        
        assert user.username == username
        assert user.habits == []

    def test_user_creation_with_habits(self):
        """Test creating a user with initial habits."""
        username = "testuser"
        user_habit1 = UserHabit(self.habit1)
        user_habit2 = UserHabit(self.habit2)
        habits = [user_habit1, user_habit2]
        
        user = User(username, habits)
        
        assert user.username == username
        assert user.habits == habits
        assert len(user.habits) == 2

    def test_get_userhabit_for_habit_exists(self):
        """Test getting UserHabit for an existing habit."""
        user = User("testuser")
        user_habit = UserHabit(self.habit1)
        user.habits = [user_habit]
        
        result = user.get_userhabit_for_habit(self.habit1)
        
        assert result == user_habit

    def test_get_userhabit_for_habit_not_exists(self):
        """Test getting UserHabit for a non-existing habit."""
        user = User("testuser")
        user_habit = UserHabit(self.habit1)
        user.habits = [user_habit]
        
        result = user.get_userhabit_for_habit(self.habit2)
        
        assert result is None

    def test_get_userhabit_for_habit_empty_habits(self):
        """Test getting UserHabit when user has no habits."""
        user = User("testuser")
        
        result = user.get_userhabit_for_habit(self.habit1)
        
        assert result is None

    def test_add_habit_success(self):
        """Test successfully adding a new habit."""
        user = User("testuser")
        
        result = user.add_habit(self.habit1)
        
        assert isinstance(result, UserHabit)
        assert result.habit == self.habit1
        assert len(user.habits) == 1
        assert user.habits[0] == result

    def test_add_habit_already_exists(self):
        """Test adding a habit that already exists raises ValueError."""
        user = User("testuser")
        user_habit = UserHabit(self.habit1)
        user.habits = [user_habit]
        
        with pytest.raises(ValueError, match=f"Habit {self.habit1.name} already exists for user testuser"):
            user.add_habit(self.habit1)

    def test_add_multiple_habits(self):
        """Test adding multiple different habits."""
        user = User("testuser")
        
        result1 = user.add_habit(self.habit1)
        result2 = user.add_habit(self.habit2)
        result3 = user.add_habit(self.habit3)
        
        assert len(user.habits) == 3
        assert all(isinstance(uh, UserHabit) for uh in user.habits)
        assert result1.habit == self.habit1
        assert result2.habit == self.habit2
        assert result3.habit == self.habit3

    def test_remove_habit_success(self):
        """Test successfully removing an existing habit."""
        user = User("testuser")
        user_habit1 = UserHabit(self.habit1)
        user_habit2 = UserHabit(self.habit2)
        user.habits = [user_habit1, user_habit2]
        
        result = user.remove_habit(self.habit1)
        
        assert result == user_habit1
        assert len(user.habits) == 1
        assert user.habits[0] == user_habit2
        assert user_habit1 not in user.habits

    def test_remove_habit_not_exists(self):
        """Test removing a habit that doesn't exist raises ValueError."""
        user = User("testuser")
        user_habit = UserHabit(self.habit1)
        user.habits = [user_habit]
        
        with pytest.raises(ValueError, match=f"Habit {self.habit2.name} does not exist for user testuser"):
            user.remove_habit(self.habit2)

    def test_remove_habit_empty_habits(self):
        """Test removing a habit when user has no habits raises ValueError."""
        user = User("testuser")
        
        with pytest.raises(ValueError, match=f"Habit {self.habit1.name} does not exist for user testuser"):
            user.remove_habit(self.habit1)

    def test_remove_all_habits(self):
        """Test removing all habits one by one."""
        user = User("testuser")
        user_habit1 = UserHabit(self.habit1)
        user_habit2 = UserHabit(self.habit2)
        user.habits = [user_habit1, user_habit2]
        
        user.remove_habit(self.habit1)
        user.remove_habit(self.habit2)
        
        assert len(user.habits) == 0

    def test_habit_name_based_matching(self):
        """Test that habit matching is based on name."""
        user = User("testuser")
        
        # Create two different Habit objects with the same name
        habit_original = Habit("Same Name", "Description 1", "daily")
        habit_duplicate = Habit("Same Name", "Description 2", "weekly")
        
        user_habit = UserHabit(habit_original)
        user.habits = [user_habit]
        
        # Should find the UserHabit even with different Habit object
        result = user.get_userhabit_for_habit(habit_duplicate)
        assert result == user_habit

    def test_json_serialization(self):
        """Test JSON serialization of User objects."""
        user = User("testuser")
        user_habit1 = UserHabit(self.habit1, userhabit_id="id1")
        user_habit2 = UserHabit(self.habit2, userhabit_id="id2")
        user.habits = [user_habit1, user_habit2]
        
        json_data = user.json()
        
        expected = {
            "username": "testuser",
            "habits": ["id1", "id2"]
        }
        
        assert json_data == expected

    def test_json_serialization_empty_habits(self):
        """Test JSON serialization of User with no habits."""
        user = User("testuser")
        
        json_data = user.json()
        
        expected = {
            "username": "testuser",
            "habits": []
        }
        
        assert json_data == expected

    def test_habit_tracking_workflow(self):
        """Test a complete workflow of adding habits and tracking them."""
        user = User("testuser")
        
        # Add habits
        user_habit1 = user.add_habit(self.habit1)
        user_habit2 = user.add_habit(self.habit2)
        
        # Track completion for one habit
        completion_time = datetime(2023, 5, 15, 12, 0, 0)
        success = user_habit1.track_completion(completion_time)
        assert success is True
        
        # Verify the habit was tracked
        retrieved_user_habit = user.get_userhabit_for_habit(self.habit1)
        assert retrieved_user_habit == user_habit1
        assert completion_time in retrieved_user_habit.completion_times
        
        # Other habit should not be affected
        other_user_habit = user.get_userhabit_for_habit(self.habit2)
        assert other_user_habit == user_habit2
        assert len(other_user_habit.completion_times) == 0

    def test_multiple_users_same_habit(self):
        """Test that multiple users can track the same habit independently."""
        user1 = User("user1")
        user2 = User("user2")
        
        # Both users add the same habit
        user_habit1 = user1.add_habit(self.habit1)
        user_habit2 = user2.add_habit(self.habit1)
        
        # They should have different UserHabit objects
        assert user_habit1 != user_habit2
        assert user_habit1.userhabit_id != user_habit2.userhabit_id
        assert user_habit1.habit == user_habit2.habit  # Same underlying habit
        
        # Track completion for one user
        completion_time = datetime(2023, 5, 15, 12, 0, 0)
        user_habit1.track_completion(completion_time)
        
        # Other user should not be affected
        assert len(user_habit1.completion_times) == 1
        assert len(user_habit2.completion_times) == 0


if __name__ == '__main__':
    pytest.main([__file__])