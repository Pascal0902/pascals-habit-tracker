import pytest
import sys
import os
import json
import tempfile
from datetime import datetime

# Add src to path for importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from data_storage.json import JsonStorageInterface
from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


class TestJsonStorageInterface:
    """Test cases for the JsonStorageInterface class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        # Write initial empty JSON structure
        json.dump({"users": {}, "habits": {}, "user_habits": {}}, self.temp_file)
        self.temp_file.close()
        self.storage = JsonStorageInterface(self.temp_file.name)
        
        # Create test data
        self.habit1 = Habit("Exercise", "Go for a run", "daily", datetime(2023, 5, 1, 10, 0, 0))
        self.habit2 = Habit("Reading", "Read a book", "weekly", datetime(2023, 5, 1, 11, 0, 0))
        self.user1 = User("testuser1")
        self.user2 = User("testuser2")

    def teardown_method(self):
        """Clean up test fixtures."""
        try:
            os.unlink(self.temp_file.name)
        except FileNotFoundError:
            pass

    def test_constructor_with_non_json_file_raises_assertion_error(self):
        """Test that constructor raises AssertionError for non-JSON files."""
        with pytest.raises(AssertionError, match="File path must be a JSON file"):
            JsonStorageInterface("test.txt")

    def test_constructor_with_existing_file(self):
        """Test constructor with existing JSON file."""
        # Create a JSON file with some data
        test_data = {"users": {"test": {}}, "habits": {}, "user_habits": {}}
        with open(self.temp_file.name, 'w') as f:
            json.dump(test_data, f)
        
        storage = JsonStorageInterface(self.temp_file.name)
        assert storage.data == test_data

    def test_constructor_with_nonexistent_file(self):
        """Test constructor with non-existent file creates default structure."""
        temp_path = self.temp_file.name.replace('.json', '_nonexistent.json')
        storage = JsonStorageInterface(temp_path)
        
        expected_data = {"users": {}, "habits": {}, "user_habits": {}}
        assert storage.data == expected_data
        
        # Clean up
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass

    def test_insert_user_success(self):
        """Test successful user insertion."""
        result = self.storage.insert_user(self.user1)
        
        assert result is True
        assert self.user1.username in self.storage.data['users']
        assert self.storage.data['users'][self.user1.username] == self.user1.json()

    def test_insert_user_already_exists(self):
        """Test inserting a user that already exists."""
        self.storage.insert_user(self.user1)
        result = self.storage.insert_user(self.user1)
        
        assert result is False

    def test_update_user_success(self):
        """Test successful user update."""
        self.storage.insert_user(self.user1)
        
        # Modify user and update
        user_habit = UserHabit(self.habit1)
        self.user1.habits = [user_habit]
        result = self.storage.update_user(self.user1)
        
        assert result is True
        assert self.storage.data['users'][self.user1.username] == self.user1.json()

    def test_update_user_not_exists(self):
        """Test updating a user that doesn't exist."""
        result = self.storage.update_user(self.user1)
        
        assert result is False

    def test_delete_user_success(self):
        """Test successful user deletion."""
        self.storage.insert_user(self.user1)
        result = self.storage.delete_user(self.user1)
        
        assert result is True
        assert self.user1.username not in self.storage.data['users']

    def test_delete_user_not_exists(self):
        """Test deleting a user that doesn't exist."""
        result = self.storage.delete_user(self.user1)
        
        assert result is False

    def test_get_user_exists(self):
        """Test getting an existing user."""
        self.storage.insert_user(self.user1)
        result = self.storage.get_user(self.user1.username)
        
        assert result is not None
        assert result.username == self.user1.username
        assert result.habits == []  # Initially empty

    def test_get_user_not_exists(self):
        """Test getting a non-existent user."""
        result = self.storage.get_user("nonexistent")
        
        assert result is None

    def test_get_user_with_habits(self):
        """Test getting a user with habits."""
        # Insert habit and user habit first
        self.storage.insert_habit(self.habit1)
        user_habit = UserHabit(self.habit1, userhabit_id="test_id")
        self.storage.insert_user_habit(user_habit)
        
        # Insert user with reference to user habit
        self.user1.habits = [user_habit]
        self.storage.insert_user(self.user1)
        
        result = self.storage.get_user(self.user1.username)
        
        assert result is not None
        assert len(result.habits) == 1
        assert result.habits[0].userhabit_id == "test_id"

    def test_insert_habit_success(self):
        """Test successful habit insertion."""
        result = self.storage.insert_habit(self.habit1)
        
        assert result is True
        assert self.habit1.name in self.storage.data['habits']
        assert self.storage.data['habits'][self.habit1.name] == self.habit1.json()

    def test_insert_habit_already_exists(self):
        """Test inserting a habit that already exists."""
        self.storage.insert_habit(self.habit1)
        result = self.storage.insert_habit(self.habit1)
        
        assert result is False

    def test_update_habit_success(self):
        """Test successful habit update."""
        self.storage.insert_habit(self.habit1)
        
        # Modify habit and update
        self.habit1.task_description = "Modified description"
        result = self.storage.update_habit(self.habit1)
        
        assert result is True
        assert self.storage.data['habits'][self.habit1.name] == self.habit1.json()

    def test_update_habit_not_exists(self):
        """Test updating a habit that doesn't exist."""
        result = self.storage.update_habit(self.habit1)
        
        assert result is False

    def test_delete_habit_success(self):
        """Test successful habit deletion."""
        self.storage.insert_habit(self.habit1)
        result = self.storage.delete_habit(self.habit1)
        
        assert result is True
        assert self.habit1.name not in self.storage.data['habits']

    def test_delete_habit_not_exists(self):
        """Test deleting a habit that doesn't exist."""
        result = self.storage.delete_habit(self.habit1)
        
        assert result is False

    def test_get_habit_exists(self):
        """Test getting an existing habit."""
        self.storage.insert_habit(self.habit1)
        result = self.storage.get_habit(self.habit1.name)
        
        assert result is not None
        assert result.name == self.habit1.name
        assert result.task_description == self.habit1.task_description
        assert result.period == self.habit1.period
        assert result.creation_time == self.habit1.creation_time

    def test_get_habit_not_exists(self):
        """Test getting a non-existent habit."""
        result = self.storage.get_habit("nonexistent")
        
        assert result is None

    def test_get_all_habits_empty(self):
        """Test getting all habits when none exist."""
        result = self.storage.get_all_habits()
        
        assert result == []

    def test_get_all_habits_multiple(self):
        """Test getting all habits when multiple exist."""
        self.storage.insert_habit(self.habit1)
        self.storage.insert_habit(self.habit2)
        
        result = self.storage.get_all_habits()
        
        assert len(result) == 2
        habit_names = [habit.name for habit in result]
        assert self.habit1.name in habit_names
        assert self.habit2.name in habit_names

    def test_insert_user_habit_success(self):
        """Test successful UserHabit insertion."""
        self.storage.insert_habit(self.habit1)
        user_habit = UserHabit(self.habit1, userhabit_id="test_id")
        
        result = self.storage.insert_user_habit(user_habit)
        
        assert result is True
        assert user_habit.userhabit_id in self.storage.data['user_habits']
        assert self.storage.data['user_habits'][user_habit.userhabit_id] == user_habit.json()

    def test_insert_user_habit_already_exists(self):
        """Test inserting a UserHabit that already exists."""
        self.storage.insert_habit(self.habit1)
        user_habit = UserHabit(self.habit1, userhabit_id="test_id")
        
        self.storage.insert_user_habit(user_habit)
        result = self.storage.insert_user_habit(user_habit)
        
        assert result is False

    def test_update_user_habit_success(self):
        """Test successful UserHabit update."""
        self.storage.insert_habit(self.habit1)
        user_habit = UserHabit(self.habit1, userhabit_id="test_id")
        self.storage.insert_user_habit(user_habit)
        
        # Modify user habit and update
        completion_time = datetime(2023, 5, 15, 12, 0, 0)
        user_habit.track_completion(completion_time)
        result = self.storage.update_user_habit(user_habit)
        
        assert result is True
        assert self.storage.data['user_habits'][user_habit.userhabit_id] == user_habit.json()

    def test_update_user_habit_not_exists(self):
        """Test updating a UserHabit that doesn't exist."""
        user_habit = UserHabit(self.habit1, userhabit_id="test_id")
        result = self.storage.update_user_habit(user_habit)
        
        assert result is False

    def test_delete_user_habit_success(self):
        """Test successful UserHabit deletion."""
        self.storage.insert_habit(self.habit1)
        user_habit = UserHabit(self.habit1, userhabit_id="test_id")
        self.storage.insert_user_habit(user_habit)
        
        result = self.storage.delete_user_habit(user_habit)
        
        assert result is True
        assert user_habit.userhabit_id not in self.storage.data['user_habits']

    def test_delete_user_habit_not_exists(self):
        """Test deleting a UserHabit that doesn't exist."""
        user_habit = UserHabit(self.habit1, userhabit_id="test_id")
        result = self.storage.delete_user_habit(user_habit)
        
        assert result is False

    def test_get_user_habit_exists(self):
        """Test getting an existing UserHabit."""
        self.storage.insert_habit(self.habit1)
        user_habit = UserHabit(self.habit1, userhabit_id="test_id")
        self.storage.insert_user_habit(user_habit)
        
        result = self.storage.get_user_habit("test_id")
        
        assert result is not None
        assert result.userhabit_id == "test_id"
        assert result.habit.name == self.habit1.name

    def test_get_user_habit_not_exists(self):
        """Test getting a non-existent UserHabit."""
        result = self.storage.get_user_habit("nonexistent")
        
        assert result is None

    def test_get_all_user_habits_empty(self):
        """Test getting all UserHabits when none exist."""
        result = self.storage.get_all_user_habits()
        
        assert result == []

    def test_get_all_user_habits_multiple(self):
        """Test getting all UserHabits when multiple exist."""
        self.storage.insert_habit(self.habit1)
        self.storage.insert_habit(self.habit2)
        
        user_habit1 = UserHabit(self.habit1, userhabit_id="id1")
        user_habit2 = UserHabit(self.habit2, userhabit_id="id2")
        
        self.storage.insert_user_habit(user_habit1)
        self.storage.insert_user_habit(user_habit2)
        
        result = self.storage.get_all_user_habits()
        
        assert len(result) == 2
        ids = [uh.userhabit_id for uh in result]
        assert "id1" in ids
        assert "id2" in ids

    def test_file_persistence(self):
        """Test that changes are persisted to file."""
        # Insert some data
        self.storage.insert_habit(self.habit1)
        self.storage.insert_user(self.user1)
        
        # Create new storage instance with same file
        new_storage = JsonStorageInterface(self.temp_file.name)
        
        # Check that data was persisted
        assert self.habit1.name in new_storage.data['habits']
        assert self.user1.username in new_storage.data['users']

    def test_directory_creation(self):
        """Test that directories are created if they don't exist."""
        # Create a path with nested directories
        nested_path = os.path.join(tempfile.gettempdir(), "test_dir", "nested", "test.json")
        
        storage = JsonStorageInterface(nested_path)
        storage.insert_habit(self.habit1)
        
        # Check that file was created
        assert os.path.exists(nested_path)
        
        # Clean up
        import shutil
        shutil.rmtree(os.path.dirname(os.path.dirname(nested_path)))

    def test_complete_workflow(self):
        """Test a complete workflow with multiple operations."""
        # Insert habits
        self.storage.insert_habit(self.habit1)
        self.storage.insert_habit(self.habit2)
        
        # Create user habits
        user_habit1 = UserHabit(self.habit1)
        user_habit2 = UserHabit(self.habit2)
        
        # Insert user habits
        self.storage.insert_user_habit(user_habit1)
        self.storage.insert_user_habit(user_habit2)
        
        # Create user with habits
        self.user1.habits = [user_habit1, user_habit2]
        self.storage.insert_user(self.user1)
        
        # Track completions
        completion_time = datetime(2023, 5, 15, 12, 0, 0)
        user_habit1.track_completion(completion_time)
        self.storage.update_user_habit(user_habit1)
        
        # Retrieve and verify
        retrieved_user = self.storage.get_user(self.user1.username)
        assert len(retrieved_user.habits) == 2
        
        # Find the updated habit
        updated_habit = None
        for uh in retrieved_user.habits:
            if uh.habit.name == self.habit1.name:
                updated_habit = uh
                break
        
        assert updated_habit is not None
        assert len(updated_habit.completion_times) == 1
        assert completion_time in updated_habit.completion_times


if __name__ == '__main__':
    pytest.main([__file__])