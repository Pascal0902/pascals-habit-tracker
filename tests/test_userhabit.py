from datetime import datetime


def test_userhabit_initialization(user_habits):
    user_habit = user_habits['5eb76a074b6a4d23bf13880eca1e05be']
    assert user_habit.userhabit_id == '5eb76a074b6a4d23bf13880eca1e05be'
    assert user_habit.habit.name == 'Morning Exercise'
    assert (
        len(user_habit.completion_times) == 25
    )  # Number of completion times in the data


def test_userhabit_period_completed(user_habits):
    user_habit = user_habits['5eb76a074b6a4d23bf13880eca1e05be']
    # Check if the habit was completed on a specific day
    period_start = datetime(2024, 9, 12)
    period_end = datetime(2024, 9, 13)
    completed = user_habit.period_completed(period_start, period_end)
    assert completed is True

    # Check for a day with no completion
    period_start = datetime(2024, 9, 6)
    period_end = datetime(2024, 9, 7)
    completed = user_habit.period_completed(period_start, period_end)
    assert completed is False


def test_userhabit_track_completion(user_habits):
    user_habit = user_habits['5eb76a074b6a4d23bf13880eca1e05be']  # Morning Exercise
    initial_count = len(user_habit.completion_times)

    # Find a date not yet completed
    test_date = datetime(2024, 10, 1)
    result = user_habit.track_completion(test_date)
    assert result is True, "Expected track_completion to return True for a new day."
    assert (
        len(user_habit.completion_times) == initial_count + 1
    ), "Expected completion_times to increase by 1."

    # Attempt to track completion again on the same day
    result = user_habit.track_completion(test_date)
    assert (
        result is False
    ), "Expected track_completion to return False when day is already completed."
    assert (
        len(user_habit.completion_times) == initial_count + 1
    ), "Expected completion_times to remain unchanged."


def test_userhabit_get_completion_history(user_habits):
    user_habit = user_habits['4f11c1d237e34e8192c5ffaa340ce65e']
    history = user_habit.get_completion_history()
    # Since it's a weekly habit starting from '2024-08-15', check the number of periods
    num_periods = len(history)
    assert num_periods > 0
    # Check if the latest period is completed
    latest_period = history[-1]
    assert latest_period[2] is False  # The last period is not completed


def test_userhabit_json(user_habits):
    user_habit = user_habits['e6e66a7d33a74e9cbdce2fcd48aa2b0f']
    user_habit_json = user_habit.json()
    assert user_habit_json['userhabit_id'] == 'e6e66a7d33a74e9cbdce2fcd48aa2b0f'
    assert user_habit_json['habit'] == 'Skill Development'
    assert len(user_habit_json['completion_times']) == 1
    assert user_habit_json['creation_time'] == '2024-08-15T09:24:05.208666'
