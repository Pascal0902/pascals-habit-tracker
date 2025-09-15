import pytest

from habit_tracking.habits import Habit


def test_user_initialization(user):
    assert user.username == 'testuser'
    assert len(user.habits) == 5


def test_user_get_userhabit_for_habit(user, habits):
    # Test retrieving a UserHabit for an existing habit
    habit = habits['Morning Exercise']
    user_habit = user.get_userhabit_for_habit(habit)
    assert user_habit is not None
    assert user_habit.habit.name == 'Morning Exercise'

    # Test retrieving a UserHabit for a non-existing habit
    new_habit = Habit(
        name='Nonexistent Habit',
        task_description='This habit does not exist',
        period='daily',
    )
    user_habit = user.get_userhabit_for_habit(new_habit)
    assert user_habit is None


def test_user_add_habit(user):
    # Add a new habit to the user
    new_habit = Habit(
        name='New Habit', task_description='Test adding a new habit', period='daily'
    )
    user_habit = user.add_habit(new_habit)
    assert user_habit.habit.name == 'New Habit'
    assert len(user.habits) == 6

    # Attempt to add the same habit again should raise ValueError
    with pytest.raises(ValueError):
        user.add_habit(new_habit)


def test_user_remove_habit(user, habits):
    # Remove an existing habit
    habit_to_remove = habits['Meal Planning']
    user.remove_habit(habit_to_remove)
    assert len(user.habits) == 4
    assert user.get_userhabit_for_habit(habit_to_remove) is None

    # Attempt to remove a habit not tracked by the user
    new_habit = Habit(
        name='Nonexistent Habit',
        task_description='This habit does not exist',
        period='daily',
    )
    with pytest.raises(ValueError):
        user.remove_habit(new_habit)


def test_user_json(user):
    user_json = user.json()
    assert user_json['username'] == 'testuser'
    assert len(user_json['habits']) == 5
    # Check that the userhabit IDs match
    habit_ids = [uh.userhabit_id for uh in user.habits]
    assert set(user_json['habits']) == set(habit_ids)
