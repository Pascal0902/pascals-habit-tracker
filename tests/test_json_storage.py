import os, sys
sys.path.append(os.path.abspath('src'))

from datetime import datetime
import pytest

from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User
from data_storage.json import JsonStorageInterface


def test_storage_requires_json_extension(tmp_path):
    with pytest.raises(AssertionError):
        JsonStorageInterface(str(tmp_path / 'data.txt'))


def test_user_operations(tmp_path):
    storage = JsonStorageInterface(str(tmp_path / 'data.json'))
    user = User('alice')
    assert storage.insert_user(user)
    assert not storage.insert_user(user)
    fetched = storage.get_user('alice')
    assert fetched.username == 'alice'
    user.habits.append(UserHabit(habit=Habit('h', 'd', 'daily')))
    assert storage.update_user(user)
    fetched = storage.get_user('alice')
    assert len(fetched.habits) == 1
    assert storage.delete_user(user)
    assert storage.get_user('alice') is None


def test_habit_operations(tmp_path):
    storage = JsonStorageInterface(str(tmp_path / 'data.json'))
    habit = Habit('h', 'desc', 'daily')
    assert storage.insert_habit(habit)
    assert not storage.insert_habit(habit)
    habit.task_description = 'new'
    assert storage.update_habit(habit)
    fetched = storage.get_habit('h')
    assert fetched.task_description == 'new'
    assert storage.get_all_habits()[0].name == 'h'
    assert storage.delete_habit(habit)
    assert storage.get_habit('h') is None


def test_user_habit_operations(tmp_path):
    storage = JsonStorageInterface(str(tmp_path / 'data.json'))
    habit = Habit('h', 'd', 'daily')
    storage.insert_habit(habit)
    user_habit = UserHabit(habit=habit)
    assert storage.insert_user_habit(user_habit)
    assert not storage.insert_user_habit(user_habit)
    user_habit.track_completion(datetime(2024, 1, 1))
    assert storage.update_user_habit(user_habit)
    fetched = storage.get_user_habit(user_habit.userhabit_id)
    assert isinstance(fetched, UserHabit)
    assert len(fetched.completion_times) == 1
    assert len(storage.get_all_user_habits()) == 1
    assert storage.delete_user_habit(user_habit)
    assert storage.get_user_habit(user_habit.userhabit_id) is None

