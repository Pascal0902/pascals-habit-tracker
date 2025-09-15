import os, sys
sys.path.append(os.path.abspath('src'))

from datetime import datetime, timedelta
import pytest

from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


@pytest.mark.parametrize(
    'period,target,start,end',
    [
        ('daily', datetime(2024, 5, 4, 15), datetime(2024, 5, 4), datetime(2024, 5, 5)),
        ('weekly', datetime(2024, 5, 4), datetime(2024, 4, 29), datetime(2024, 5, 6)),
        ('monthly', datetime(2024, 5, 15), datetime(2024, 5, 1), datetime(2024, 6, 1)),
        ('quarterly', datetime(2024, 7, 10), datetime(2024, 7, 1), datetime(2024, 10, 1)),
        ('annually', datetime(2024, 5, 15), datetime(2024, 1, 1), datetime(2025, 1, 1)),
    ],
)
def test_get_period_start_end(period, target, start, end):
    habit = Habit('h', 'd', period)
    s, e = habit.get_period_start_end(target)
    assert s == start and e == end


def test_get_next_period():
    habit = Habit('h', 'd', 'monthly')
    next_start, next_end = habit.get_next_period(datetime(2024, 12, 1))
    assert next_start == datetime(2024, 12, 1)
    assert next_end == datetime(2025, 1, 1)


@pytest.fixture
def fixed_datetime(monkeypatch):
    from habit_tracking import habits as habits_module

    fixed_now = datetime(2024, 1, 15)

    class FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now

    monkeypatch.setattr(habits_module, 'datetime', FixedDateTime)
    return fixed_now


def test_get_all_periods_since(fixed_datetime):
    habit = Habit('h', 'd', 'daily')
    start_time = fixed_datetime - timedelta(days=2, hours=1)
    periods = habit.get_all_periods_since(start_time)
    assert [p[0] for p in periods] == [
        datetime(2024, 1, 12),
        datetime(2024, 1, 13),
        datetime(2024, 1, 14),
    ]


def test_habit_json():
    creation = datetime(2024, 1, 1)
    habit = Habit('h', 'desc', 'monthly', creation)
    assert habit.json() == {
        'name': 'h',
        'task_description': 'desc',
        'period': 'monthly',
        'creation_time': creation.isoformat(),
    }


def test_userhabit_track_completion():
    habit = Habit('h', 'd', 'daily')
    user_habit = UserHabit(habit=habit)
    time = datetime(2024, 1, 10, 10)
    assert user_habit.track_completion(time)
    assert not user_habit.track_completion(time + timedelta(hours=1))
    assert user_habit.track_completion(time + timedelta(days=1))


def test_userhabit_completion_history(fixed_datetime):
    habit = Habit('h', 'd', 'daily')
    creation = fixed_datetime - timedelta(days=2)
    user_habit = UserHabit(habit=habit, creation_time=creation)
    user_habit.track_completion(creation + timedelta(hours=1))
    history = user_habit.get_completion_history()
    assert history[0][2] is True
    assert history[1][2] is False


def test_userhabit_json():
    habit = Habit('h', 'd', 'daily')
    user_habit = UserHabit(habit=habit)
    data = user_habit.json()
    assert data['habit'] == 'h'
    assert data['userhabit_id'] == user_habit.userhabit_id


def test_user_add_remove_habit():
    habit = Habit('h', 'd', 'daily')
    user = User('alice')
    user_habit = user.add_habit(habit)
    assert user.get_userhabit_for_habit(habit) == user_habit
    with pytest.raises(ValueError):
        user.add_habit(habit)
    removed = user.remove_habit(habit)
    assert removed == user_habit
    with pytest.raises(ValueError):
        user.remove_habit(habit)


def test_user_json():
    habit = Habit('h', 'd', 'daily')
    user = User('alice', habits=[UserHabit(habit=habit, userhabit_id='123')])
    assert user.json() == {'username': 'alice', 'habits': ['123']}
