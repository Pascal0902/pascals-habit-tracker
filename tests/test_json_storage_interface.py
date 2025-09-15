from datetime import datetime

import pytest

from data_storage.json import JsonStorageInterface
from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


@pytest.fixture
def storage(tmp_path):
    file_path = tmp_path / "test_data.json"
    return JsonStorageInterface(str(file_path))


def test_insert_user(storage):
    user = User(username="test_user")
    result = storage.insert_user(user)
    assert result == True
    # Try inserting the same user again
    result = storage.insert_user(user)
    assert result == False


def test_get_user(storage):
    user = User(username="test_user")
    storage.insert_user(user)
    retrieved_user = storage.get_user("test_user")
    assert retrieved_user.username == "test_user"
    assert retrieved_user.habits == []
    # Try retrieving a non-existing user
    assert storage.get_user("nonexistent_user") is None


def test_update_user(storage):
    user = User(username="test_user")
    # Update before inserting should return False
    result = storage.update_user(user)
    assert result == False
    storage.insert_user(user)
    # Create a Habit and insert it into storage
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    storage.insert_habit(habit)
    # Add habit to user and insert UserHabit into storage
    user_habit = user.add_habit(habit)
    storage.insert_user_habit(user_habit)
    # Update user in storage
    result = storage.update_user(user)
    assert result == True
    # Retrieve user
    retrieved_user = storage.get_user("test_user")
    assert len(retrieved_user.habits) == 1
    assert retrieved_user.habits[0].userhabit_id == user_habit.userhabit_id


def test_delete_user(storage):
    user = User(username="test_user")
    # Delete before inserting should return False
    result = storage.delete_user(user)
    assert result == False
    storage.insert_user(user)
    result = storage.delete_user(user)
    assert result == True
    assert storage.get_user("test_user") is None


def test_insert_habit(storage):
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    result = storage.insert_habit(habit)
    assert result == True
    # Try inserting the same habit again
    result = storage.insert_habit(habit)
    assert result == False


def test_get_habit(storage):
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    storage.insert_habit(habit)
    retrieved_habit = storage.get_habit("Exercise")
    assert retrieved_habit.name == "Exercise"
    assert retrieved_habit.task_description == "Do 30 minutes of exercise"
    assert retrieved_habit.period == "daily"
    # Try retrieving a non-existing habit
    assert storage.get_habit("Nonexistent") is None


def test_update_habit(storage):
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    # Update before inserting should return False
    result = storage.update_habit(habit)
    assert result == False
    storage.insert_habit(habit)
    habit.task_description = "Do 45 minutes of exercise"
    result = storage.update_habit(habit)
    assert result == True
    retrieved_habit = storage.get_habit("Exercise")
    assert retrieved_habit.task_description == "Do 45 minutes of exercise"


def test_delete_habit(storage):
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    # Delete before inserting should return False
    result = storage.delete_habit(habit)
    assert result == False
    storage.insert_habit(habit)
    result = storage.delete_habit(habit)
    assert result == True
    assert storage.get_habit("Exercise") is None


def test_get_all_habits(storage):
    habit1 = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    habit2 = Habit(
        name="Read", task_description="Read a book for 1 hour", period="daily"
    )
    storage.insert_habit(habit1)
    storage.insert_habit(habit2)
    habits = storage.get_all_habits()
    assert len(habits) == 2
    habit_names = [habit.name for habit in habits]
    assert "Exercise" in habit_names
    assert "Read" in habit_names


def test_insert_user_habit(storage):
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    storage.insert_habit(habit)
    user_habit = UserHabit(habit=habit)
    result = storage.insert_user_habit(user_habit)
    assert result == True
    # Try inserting the same user_habit again
    result = storage.insert_user_habit(user_habit)
    assert result == False


def test_get_user_habit(storage):
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    storage.insert_habit(habit)
    user_habit = UserHabit(habit=habit)
    storage.insert_user_habit(user_habit)
    retrieved_user_habit = storage.get_user_habit(user_habit.userhabit_id)
    assert retrieved_user_habit.userhabit_id == user_habit.userhabit_id
    assert retrieved_user_habit.habit.name == "Exercise"
    # Try retrieving a non-existing user_habit
    assert storage.get_user_habit("nonexistent") is None


def test_update_user_habit(storage):
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    storage.insert_habit(habit)
    user_habit = UserHabit(habit=habit)
    # Update before inserting should return False
    result = storage.update_user_habit(user_habit)
    assert result == False
    storage.insert_user_habit(user_habit)
    # Add a completion time
    completion_time = datetime(2021, 1, 1, 12, 0, 0)
    user_habit.completion_times.append(completion_time)
    result = storage.update_user_habit(user_habit)
    assert result == True
    retrieved_user_habit = storage.get_user_habit(user_habit.userhabit_id)
    assert len(retrieved_user_habit.completion_times) == 1
    assert retrieved_user_habit.completion_times[0] == completion_time


def test_delete_user_habit(storage):
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    storage.insert_habit(habit)
    user_habit = UserHabit(habit=habit)
    # Delete before inserting should return False
    result = storage.delete_user_habit(user_habit)
    assert result == False
    storage.insert_user_habit(user_habit)
    result = storage.delete_user_habit(user_habit)
    assert result == True
    assert storage.get_user_habit(user_habit.userhabit_id) is None


def test_get_all_user_habits(storage):
    habit1 = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    habit2 = Habit(
        name="Read", task_description="Read a book for 1 hour", period="daily"
    )
    storage.insert_habit(habit1)
    storage.insert_habit(habit2)
    user_habit1 = UserHabit(habit=habit1)
    user_habit2 = UserHabit(habit=habit2)
    storage.insert_user_habit(user_habit1)
    storage.insert_user_habit(user_habit2)
    user_habits = storage.get_all_user_habits()
    assert len(user_habits) == 2
    user_habit_ids = [uh.userhabit_id for uh in user_habits]
    assert user_habit1.userhabit_id in user_habit_ids
    assert user_habit2.userhabit_id in user_habit_ids


def test_get_user_with_habits(storage):
    # Create habit and insert it
    habit = Habit(
        name="Exercise", task_description="Do 30 minutes of exercise", period="daily"
    )
    storage.insert_habit(habit)
    # Create user habit and insert it
    user_habit = UserHabit(habit=habit)
    storage.insert_user_habit(user_habit)
    # Create user and add habit
    user = User(username="test_user")
    user.habits.append(user_habit)
    # Insert user
    storage.insert_user(user)
    # Retrieve user
    retrieved_user = storage.get_user("test_user")
    assert retrieved_user.username == "test_user"
    assert len(retrieved_user.habits) == 1
    assert retrieved_user.habits[0].userhabit_id == user_habit.userhabit_id
    assert retrieved_user.habits[0].habit.name == "Exercise"


def test_data_persistence(tmp_path):
    file_path = tmp_path / "test_data.json"
    storage1 = JsonStorageInterface(str(file_path))
    user = User(username="test_user")
    storage1.insert_user(user)
    storage2 = JsonStorageInterface(str(file_path))
    retrieved_user = storage2.get_user("test_user")
    assert retrieved_user is not None
    assert retrieved_user.username == "test_user"


def test_init_with_non_json_file(tmp_path):
    file_path = tmp_path / "test_data.txt"
    with pytest.raises(AssertionError):
        JsonStorageInterface(str(file_path))
