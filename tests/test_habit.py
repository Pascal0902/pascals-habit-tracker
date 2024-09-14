from datetime import datetime

from habit_tracking.habits import Habit


def test_habit_initialization(habits):
    habit = habits['Morning Exercise']
    assert habit.name == 'Morning Exercise'
    assert (
        habit.task_description
        == 'Exercise every morning to boost your energy and stay healthy'
    )
    assert habit.period == 'daily'


def test_habit_get_period_start_end():
    habit = Habit(
        name='Test Habit', task_description='Test period calculation', period='weekly'
    )
    target_time = datetime(2024, 9, 10)  # Assume it's a Tuesday
    start, end = habit.get_period_start_end(target_time)
    assert start == datetime(2024, 9, 9)  # Week starts on Monday
    assert end == datetime(2024, 9, 16)


def test_habit_json(habits):
    habit = habits['Budget Review']
    habit_json = habit.json()
    assert habit_json['name'] == 'Budget Review'
    assert (
        habit_json['task_description']
        == 'Review your income and expenses every month to keep track of your finances'
    )
    assert habit_json['period'] == 'monthly'
    assert habit_json['creation_time'] == '2024-09-13T12:09:08.591386'
