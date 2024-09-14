import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_dir = os.path.join(root_dir, 'src')

sys.path.insert(0, src_dir)


import json
from datetime import datetime
from pathlib import Path

import pytest

from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


@pytest.fixture
def json_data():
    # Load the JSON data from the file
    data_file = Path('tests/test_data.json')
    with open(data_file, 'r') as f:
        data = json.load(f)
    return data


@pytest.fixture
def habits(json_data):
    # Create Habit instances from the JSON data
    habits = {}
    for habit_name, habit_data in json_data['habits'].items():
        habit = Habit(
            name=habit_data['name'],
            task_description=habit_data['task_description'],
            period=habit_data['period'],
            creation_time=datetime.fromisoformat(habit_data['creation_time']),
        )
        habits[habit_name] = habit
    return habits


@pytest.fixture
def user_habits(json_data, habits):
    # Create UserHabit instances from the JSON data
    user_habits = {}
    for uh_id, uh_data in json_data['user_habits'].items():
        habit = habits[uh_data['habit']]
        completion_times = [
            datetime.fromisoformat(ct) for ct in uh_data['completion_times']
        ]
        user_habit = UserHabit(
            habit=habit,
            userhabit_id=uh_id,
            completion_times=completion_times,
            creation_time=datetime.fromisoformat(uh_data['creation_time']),
        )
        user_habits[uh_id] = user_habit
    return user_habits


@pytest.fixture
def user(json_data, user_habits):
    # Create User instance from the JSON data
    user_data = json_data['users']['testuser']
    user_habits_list = [user_habits[uh_id] for uh_id in user_data['habits']]
    user = User(username=user_data['username'], habits=user_habits_list)
    return user
