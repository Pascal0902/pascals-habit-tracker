

import pytest
from src.habit_tracking.users import User
from src.habit_tracking.habits import UserHabit, Habit
from datetime import datetime

@pytest.fixture
def sample_habit():
    return Habit("Test Habit", "Description for test habit", "daily", datetime(2023, 1, 1))

@pytest.fixture
def sample_user_habit(sample_habit):
    return UserHabit(sample_habit, userhabit_id="uh1", creation_time=datetime(2023, 1, 15))

def test_user_initialization():
    user = User("testuser")
    assert user.username == "testuser"
    assert user.habits == []

def test_user_initialization_with_habits(sample_user_habit):
    user = User("testuser", habits=[sample_user_habit])
    assert user.username == "testuser"
    assert len(user.habits) == 1
    assert user.habits[0] == sample_user_habit

def test_user_initialization_with_duplicate_habits():
    habit = Habit("Test Habit", "Desc", "daily", datetime(2023, 1, 1))
    uh1 = UserHabit(habit, userhabit_id="uh1", creation_time=datetime(2023, 1, 15))
    uh1_duplicate = UserHabit(habit, userhabit_id="uh1", creation_time=datetime(2023, 1, 16)) # Same ID, different creation time
    user = User("testuser", habits=[uh1, uh1_duplicate])
    assert len(user.habits) == 1
    assert user.habits[0] == uh1 # Should keep the first one

def test_user_json_representation(sample_user_habit):
    user = User("testuser", habits=[sample_user_habit])
    expected_json = {
        "username": "testuser",
        "habits": ["uh1"]
    }
    assert user.json() == expected_json

def test_user_add_habit_success(sample_habit):
    user = User("testuser")
    user_habit = user.add_habit(sample_habit)
    assert len(user.habits) == 1
    assert user.habits[0].habit == sample_habit
    assert user_habit.habit == sample_habit

def test_user_add_duplicate_habit_raises_error(sample_habit):
    user = User("testuser")
    user.add_habit(sample_habit)
    with pytest.raises(ValueError, match=f"Habit {sample_habit.name} already exists for user testuser"):
        user.add_habit(sample_habit)

def test_user_get_user_habit_by_id_success(sample_user_habit):
    user = User("testuser", habits=[sample_user_habit])
    retrieved_habit = user.get_user_habit("uh1")
    assert retrieved_habit == sample_user_habit

def test_user_get_user_habit_by_id_not_found():
    user = User("testuser")
    retrieved_habit = user.get_user_habit("nonexistent_id")
    assert retrieved_habit is None

def test_user_update_user_habit_success(sample_habit):
    initial_user_habit = UserHabit(sample_habit, userhabit_id="uh1", completion_times=[], creation_time=datetime(2023, 1, 15))
    user = User("testuser", habits=[initial_user_habit])

    updated_completion_times = [datetime(2023, 1, 16)]
    updated_user_habit = UserHabit(sample_habit, userhabit_id="uh1", completion_times=updated_completion_times, creation_time=datetime(2023, 1, 15))

    assert user.update_user_habit(updated_user_habit) is True
    retrieved_habit = user.get_user_habit("uh1")
    assert retrieved_habit.completion_times == updated_completion_times

def test_user_update_user_habit_non_existent_returns_false(sample_user_habit):
    user = User("testuser") # User has no habits
    updated_user_habit = UserHabit(sample_user_habit.habit, userhabit_id="uh_nonexistent", completion_times=[], creation_time=datetime.now())
    assert user.update_user_habit(updated_user_habit) is False
    assert user.get_user_habit("uh_nonexistent") is None

def test_user_delete_user_habit_success(sample_user_habit):
    user = User("testuser", habits=[sample_user_habit])
    assert user.delete_user_habit("uh1") is True
    assert user.habits == []
    assert user.get_user_habit("uh1") is None

def test_user_delete_user_habit_non_existent_returns_false(sample_user_habit):
    user = User("testuser") # User has no habits
    assert user.delete_user_habit("nonexistent_id") is False
    assert user.habits == []

def test_user_remove_habit_success(sample_habit, sample_user_habit):
    user = User("testuser", habits=[sample_user_habit])
    removed_habit = user.remove_habit(sample_habit)
    assert removed_habit == sample_user_habit
    assert user.habits == []

def test_user_remove_habit_non_existent_raises_error(sample_habit):
    user = User("testuser")
    with pytest.raises(ValueError, match=f"Habit {sample_habit.name} does not exist for user testuser"):
        user.remove_habit(sample_habit)


