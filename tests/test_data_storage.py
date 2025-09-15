
import pytest
import os
import json
from datetime import datetime
from src.data_storage.json import JsonStorageInterface
from src.habit_tracking.users import User
from src.habit_tracking.habits import Habit, UserHabit


@pytest.fixture
def temp_json_file(tmp_path):
    file_path = tmp_path / "test_data.json"
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def storage_instance(temp_json_file):
    return JsonStorageInterface(str(temp_json_file))


def test_initialization_empty_file(tmp_path):
    file_path = tmp_path / "test_data.json"
    storage = JsonStorageInterface(str(file_path))
    expected_initial_data = {"users": {}, "habits": {}, "user_habits": {}}
    assert storage.data == expected_initial_data
    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        assert json.load(f) == expected_initial_data


def test_initialization_with_existing_data(storage_instance, temp_json_file):
    initial_data = {"users": {"testuser": {"username": "testuser", "habits": []}}, "habits": {}, "user_habits": {}}
    with open(temp_json_file, 'w') as f:
        json.dump(initial_data, f)

    storage = JsonStorageInterface(str(temp_json_file))
    assert storage.data == initial_data


def test_insert_user_success(storage_instance):
    user = User("testuser")
    assert storage_instance.insert_user(user) is True
    assert storage_instance.data["users"]["testuser"]["username"] == "testuser"
    assert storage_instance.get_user("testuser").username == "testuser"

def test_insert_user_duplicate(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    assert storage_instance.insert_user(user) is False

def test_update_user_success(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    # The User object only has username and habits (list of userhabit_ids)
    # To truly "update" a user, we would typically modify their associated habits.
    # For this test, we confirm the method returns True for an existing user.
    # The primary data in `User` is its username, which is the key, so updating
    # the user object itself without changing the username doesn't visibly alter
    # the stored data through `User.json()` unless its internal habits list changes.
    updated_user = User("testuser")
    assert storage_instance.update_user(updated_user) is True
    # Verify the user still exists and its fundamental properties are unchanged
    retrieved_user = storage_instance.get_user("testuser")
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    # To check persistence, we can re-initialize and check
    reloaded_storage = JsonStorageInterface(storage_instance.file_path)
    reloaded_user = reloaded_storage.get_user("testuser")
    assert reloaded_user.username == "testuser"

def test_update_user_non_existent(storage_instance):
    user = User("nonexistent")
    assert storage_instance.update_user(user) is False

def test_delete_user_success(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    assert storage_instance.delete_user(user) is True
    assert "testuser" not in storage_instance.data["users"]
    assert storage_instance.get_user("testuser") is None

def test_delete_user_non_existent(storage_instance):
    user = User("nonexistent")
    assert storage_instance.delete_user(user) is False

def test_get_user_success(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    retrieved_user = storage_instance.get_user("testuser")
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"

def test_get_user_non_existent(storage_instance):
    assert storage_instance.get_user("nonexistent") is None


def test_insert_habit_success(storage_instance):
    habit = Habit("Read Book", "Read 30 pages daily", "daily", datetime.now())
    assert storage_instance.insert_habit(habit) is True
    assert storage_instance.data["habits"]["Read Book"]["name"] == "Read Book"
    assert storage_instance.get_habit("Read Book").name == "Read Book"

def test_insert_habit_duplicate(storage_instance):
    habit = Habit("Read Book", "Read 30 pages daily", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    assert storage_instance.insert_habit(habit) is False

def test_update_habit_success(storage_instance):
    habit = Habit("Read Book", "Read 30 pages daily", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    updated_habit = Habit("Read Book", "Read 50 pages daily", "daily", datetime.now())
    assert storage_instance.update_habit(updated_habit) is True
    assert storage_instance.data["habits"]["Read Book"]["task_description"] == "Read 50 pages daily"
    # Re-load to ensure changes are persistent
    reloaded_storage = JsonStorageInterface(storage_instance.file_path)
    reloaded_habit = reloaded_storage.get_habit("Read Book")
    assert reloaded_habit.task_description == "Read 50 pages daily"

def test_update_habit_non_existent(storage_instance):
    habit = Habit("nonexistent", "desc", "daily", datetime.now())
    assert storage_instance.update_habit(habit) is False

def test_delete_habit_success(storage_instance):
    habit = Habit("Read Book", "Read 30 pages daily", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    assert storage_instance.delete_habit(habit) is True
    assert "Read Book" not in storage_instance.data["habits"]
    assert storage_instance.get_habit("Read Book") is None

def test_delete_habit_non_existent(storage_instance):
    habit = Habit("nonexistent", "desc", "daily", datetime.now())
    assert storage_instance.delete_habit(habit) is False

def test_get_habit_success(storage_instance):
    habit = Habit("Read Book", "Read 30 pages daily", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    retrieved_habit = storage_instance.get_habit("Read Book")
    assert retrieved_habit is not None
    assert retrieved_habit.name == "Read Book"

def test_get_habit_non_existent(storage_instance):
    assert storage_instance.get_habit("nonexistent") is None

def test_get_all_habits_empty(storage_instance):
    assert storage_instance.get_all_habits() == []

def test_get_all_habits_with_data(storage_instance):
    habit1 = Habit("Read Book", "desc1", "daily", datetime(2023, 1, 1))
    habit2 = Habit("Exercise", "desc2", "weekly", datetime(2023, 1, 2))
    storage_instance.insert_habit(habit1)
    storage_instance.insert_habit(habit2)
    all_habits = storage_instance.get_all_habits()
    assert len(all_habits) == 2
    assert any(h.name == "Read Book" for h in all_habits)
    assert any(h.name == "Exercise" for h in all_habits)

def test_insert_user_habit_success(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    habit = Habit("Read Book", "desc", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    user_habit = UserHabit(habit, userhabit_id="uh1", completion_times=[], creation_time=datetime.now())
    assert storage_instance.insert_user_habit(user_habit) is True
    assert storage_instance.data["user_habits"]["uh1"]["userhabit_id"] == "uh1"
    assert storage_instance.get_user_habit("uh1").userhabit_id == "uh1"

def test_insert_user_habit_duplicate(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    habit = Habit("Read Book", "desc", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    user_habit = UserHabit(habit, userhabit_id="uh1", completion_times=[], creation_time=datetime.now())
    storage_instance.insert_user_habit(user_habit)
    assert storage_instance.insert_user_habit(user_habit) is False

def test_update_user_habit_success(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    habit = Habit("Read Book", "desc", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    user_habit = UserHabit(habit, userhabit_id="uh1", completion_times=[], creation_time=datetime.now())
    storage_instance.insert_user_habit(user_habit)

    updated_user_habit = UserHabit(habit, userhabit_id="uh1", completion_times=[datetime.now()], creation_time=datetime.now())
    assert storage_instance.update_user_habit(updated_user_habit) is True
    assert len(storage_instance.data["user_habits"]["uh1"]["completion_times"]) == 1
    # Re-load to ensure changes are persistent
    reloaded_storage = JsonStorageInterface(storage_instance.file_path)
    reloaded_user_habit = reloaded_storage.get_user_habit("uh1")
    assert len(reloaded_user_habit.completion_times) == 1

def test_update_user_habit_non_existent(storage_instance):
    habit = Habit("Read Book", "desc", "daily", datetime.now())
    user_habit = UserHabit(habit, userhabit_id="uh_nonexistent", completion_times=[], creation_time=datetime.now())
    assert storage_instance.update_user_habit(user_habit) is False

def test_delete_user_habit_success(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    habit = Habit("Read Book", "desc", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    user_habit = UserHabit(habit, userhabit_id="uh1", completion_times=[], creation_time=datetime.now())
    storage_instance.insert_user_habit(user_habit)
    assert storage_instance.delete_user_habit(user_habit) is True
    assert "uh1" not in storage_instance.data["user_habits"]
    assert storage_instance.get_user_habit("uh1") is None

def test_delete_user_habit_non_existent(storage_instance):
    habit = Habit("Read Book", "desc", "daily", datetime.now())
    user_habit = UserHabit(habit, userhabit_id="uh_nonexistent", completion_times=[], creation_time=datetime.now())
    assert storage_instance.delete_user_habit(user_habit) is False

def test_get_user_habit_success(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    habit = Habit("Read Book", "desc", "daily", datetime.now())
    storage_instance.insert_habit(habit)
    user_habit = UserHabit(habit, userhabit_id="uh1", completion_times=[], creation_time=datetime.now())
    storage_instance.insert_user_habit(user_habit)
    retrieved_user_habit = storage_instance.get_user_habit("uh1")
    assert retrieved_user_habit is not None
    assert retrieved_user_habit.userhabit_id == "uh1"

def test_get_user_habit_non_existent(storage_instance):
    assert storage_instance.get_user_habit("nonexistent") is None

def test_get_all_user_habits_empty(storage_instance):
    assert storage_instance.get_all_user_habits() == []

def test_get_all_user_habits_with_data(storage_instance):
    user = User("testuser")
    storage_instance.insert_user(user)
    habit1 = Habit("Read Book", "desc1", "daily", datetime(2023, 1, 1))
    habit2 = Habit("Exercise", "desc2", "weekly", datetime(2023, 1, 2))
    storage_instance.insert_habit(habit1)
    storage_instance.insert_habit(habit2)

    user_habit1 = UserHabit(habit1, userhabit_id="uh1", completion_times=[], creation_time=datetime(2023, 1, 1))
    user_habit2 = UserHabit(habit2, userhabit_id="uh2", completion_times=[datetime(2023, 1, 3)], creation_time=datetime(2023, 1, 2))
    storage_instance.insert_user_habit(user_habit1)
    storage_instance.insert_user_habit(user_habit2)

    all_user_habits = storage_instance.get_all_user_habits()
    assert len(all_user_habits) == 2
    assert any(uh.userhabit_id == "uh1" for uh in all_user_habits)
    assert any(uh.userhabit_id == "uh2" for uh in all_user_habits)

