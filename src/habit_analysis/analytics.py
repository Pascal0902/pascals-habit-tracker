"""Utility functions for analysing habit tracking statistics.

The module exposes helpers to determine current and longest streaks for
``UserHabit`` instances as well as convenience functions operating on an entire
``User``.  The internal helper functions return streak lengths from a completion
history and are reused by the public API.
"""

from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


def _longest_streak_from_history(
    completion_history: list[tuple[object, object, bool]]
) -> int:
    """Return the longest streak from a completion history.

    The ``completion_history`` list is expected to contain tuples of
    ``(period_start, period_end, completed)``. Only the ``completed`` flag is
    used for the calculation.
    """
    longest = 0
    current = 0
    for _, _, completed in completion_history:
        if completed:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def _current_streak_from_history(
    completion_history: list[tuple[object, object, bool]]
) -> int:
    """Return the current streak from a completion history.

    Incomplete periods at the end of the history are ignored before counting
    consecutive ``True`` entries from the back of the list.
    """
    if completion_history and not completion_history[-1][2]:
        completion_history = completion_history[:-1]
    current = 0
    for _, _, completed in reversed(completion_history):
        if completed:
            current += 1
        else:
            break
    return current


def get_all_tracked_habits_with_streak(user: User) -> list[tuple[Habit, int]]:
    """
    Retrieve all habits tracked by the user with their current streaks.
    Args:
        user: The user to retrieve habits for.

    Returns:
        A list of tuples containing the habit and its current streak.
    """
    habits_with_streak = []
    for user_habit in user.habits:
        history = user_habit.get_completion_history()
        current_streak = _current_streak_from_history(history)
        habits_with_streak.append((user_habit.habit, current_streak))
    return habits_with_streak


def get_all_tracked_habits_with_streak_for_periodicity(
    user: User, period: str
) -> list[tuple[Habit, int]]:
    """
    Retrieve all habits tracked by the user with their current streaks for a specific periodicity.
    Args:
        user: The user to retrieve habits for.
        period: The periodicity to retrieve habits for.

    Returns:
        A list of tuples containing the habit and its current streak.
    """
    habits_with_streak = []
    for user_habit in user.habits:
        if user_habit.habit.period == period:
            history = user_habit.get_completion_history()
            current_streak = _current_streak_from_history(history)
            habits_with_streak.append((user_habit.habit, current_streak))
    return habits_with_streak


def get_all_time_longest_habit_streak(user: User) -> tuple[Habit, int]:
    """
    Retrieve the habit with the longest streak tracked by the user.
    Args:
        user: The user to retrieve habits for.

    Returns:
        A tuple containing the habit with the longest streak and the length of the streak.
    """
    longest_streak = (None, 0)
    for user_habit in user.habits:
        history = user_habit.get_completion_history()
        streak = _longest_streak_from_history(history)
        if streak > longest_streak[1]:
            longest_streak = (user_habit.habit, streak)
    return longest_streak


def get_current_longest_habit_streak(user: User) -> tuple[Habit, int]:
    """
    Retrieve the habit with the longest current streak tracked by the user.
    Args:
        user: The user to retrieve habits for.

    Returns:
        A tuple containing the habit with the longest current streak and the length of the streak.
    """
    longest_streak = (None, 0)
    for user_habit in user.habits:
        history = user_habit.get_completion_history()
        current = _current_streak_from_history(history)
        if current > longest_streak[1]:
            longest_streak = (user_habit.habit, current)
    return longest_streak


def get_longest_streak_for_habit(user_habit: UserHabit) -> int:
    """
    Retrieve the longest streak for a specific habit tracked by the user.
    Args:
        user_habit: The UserHabit to retrieve the longest streak for.

    Returns:
        The length of the longest streak for the habit.
    """
    history = user_habit.get_completion_history()
    return _longest_streak_from_history(history)


def get_current_streak_for_habit(user_habit: UserHabit) -> int:
    """
    Retrieve the current streak for a specific habit tracked by the user.
    Args:
        user_habit: The UserHabit to retrieve the current streak for.

    Returns:
        The length of the current streak for the habit.
    """
    history = user_habit.get_completion_history()
    return _current_streak_from_history(history)
