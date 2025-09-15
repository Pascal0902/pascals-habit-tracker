import os, sys
sys.path.append(os.path.abspath('src'))

from datetime import datetime, timedelta

import pytest

from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User
from habit_analysis.analytics import (
    get_all_tracked_habits_with_streak,
    get_all_tracked_habits_with_streak_for_periodicity,
    get_all_time_longest_habit_streak,
    get_current_longest_habit_streak,
    get_longest_streak_for_habit,
    get_current_streak_for_habit,
)


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


def build_user(fixed_datetime):
    daily = Habit('daily', 'd', 'daily')
    weekly = Habit('weekly', 'd', 'weekly')
    uh_daily = UserHabit(habit=daily, creation_time=fixed_datetime - timedelta(days=5))
    for days in [5, 4, 3, 2]:
        uh_daily.track_completion(fixed_datetime - timedelta(days=days))
    uh_weekly = UserHabit(habit=weekly, creation_time=fixed_datetime - timedelta(days=21))
    uh_weekly.track_completion(fixed_datetime - timedelta(days=15))
    uh_weekly.track_completion(fixed_datetime - timedelta(days=8))
    user = User('alice', habits=[uh_daily, uh_weekly])
    return user, uh_daily, uh_weekly


def test_get_all_tracked_habits_with_streak(fixed_datetime):
    user, uh_daily, uh_weekly = build_user(fixed_datetime)
    result = get_all_tracked_habits_with_streak(user)
    assert result == [(uh_daily.habit, 4), (uh_weekly.habit, 2)]


def test_get_all_tracked_habits_with_streak_for_periodicity(fixed_datetime):
    user, uh_daily, uh_weekly = build_user(fixed_datetime)
    result = get_all_tracked_habits_with_streak_for_periodicity(user, 'daily')
    assert result == [(uh_daily.habit, 4)]


def test_longest_streaks(fixed_datetime):
    user, uh_daily, uh_weekly = build_user(fixed_datetime)
    habit, streak = get_all_time_longest_habit_streak(user)
    assert habit == uh_daily.habit and streak == 4
    habit, streak = get_current_longest_habit_streak(user)
    assert habit == uh_daily.habit and streak == 4
    assert get_longest_streak_for_habit(uh_weekly) == 2
    assert get_current_streak_for_habit(uh_weekly) == 2
