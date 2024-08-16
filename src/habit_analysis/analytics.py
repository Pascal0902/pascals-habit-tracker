from ..habit_tracking.users import User
from ..habit_tracking.habits import Habit, UserHabit


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
        completion_history = user_habit.get_completion_history()
        current_streak = 0
        for _, _, completed in reversed(completion_history[:-1]):  # :-1 to exclude the current period
            if completed:
                current_streak += 1
            else:
                break
        habits_with_streak.append((user_habit.habit, current_streak))
    return habits_with_streak


def get_all_tracked_habits_with_streak_for_periodicity(user: User, period: str) -> list[tuple[Habit, int]]:
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
            completion_history = user_habit.get_completion_history()
            # Remove the current period if it is not yet completed
            completion_history = completion_history if completion_history[-1][2] else completion_history[:-1]
            current_streak = 0
            for _, _, completed in reversed(completion_history):
                if completed:
                    current_streak += 1
                else:
                    break
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
        completion_history = user_habit.get_completion_history()
        longest_streak_for_habit = 0
        current_streak = 0
        for _, _, completed in completion_history:
            if completed:
                current_streak += 1
            else:
                longest_streak_for_habit = max(longest_streak_for_habit, current_streak)
                current_streak = 0
        longest_streak_for_habit = max(longest_streak_for_habit, current_streak)
        if longest_streak_for_habit > longest_streak[1]:
            longest_streak = (user_habit.habit, longest_streak_for_habit)
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
        completion_history = user_habit.get_completion_history()
        # Remove the current period if it is not yet completed
        completion_history = completion_history if completion_history[-1][2] else completion_history[:-1]
        current_streak = 0
        for _, _, completed in reversed(completion_history):
            if completed:
                current_streak += 1
            else:
                break
        if current_streak > longest_streak[1]:
            longest_streak = (user_habit.habit, current_streak)
    return longest_streak


def get_longest_streak_for_habit(user_habit: UserHabit) -> int:
    """
    Retrieve the longest streak for a specific habit tracked by the user.
    Args:
        user_habit: The UserHabit to retrieve the longest streak for.

    Returns:
        The length of the longest streak for the habit.
    """
    completion_history = user_habit.get_completion_history()
    longest_streak = 0
    current_streak = 0
    for _, _, completed in completion_history:
        if completed:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 0
    longest_streak = max(longest_streak, current_streak)
    return longest_streak


def get_current_streak_for_habit(user_habit: UserHabit) -> int:
    """
    Retrieve the current streak for a specific habit tracked by the user.
    Args:
        user_habit: The UserHabit to retrieve the current streak for.

    Returns:
        The length of the current streak for the habit.
    """
    completion_history = user_habit.get_completion_history()
    # Remove the current period if it is not yet completed
    completion_history = completion_history if completion_history[-1][2] else completion_history[:-1]
    current_streak = 0
    for _, _, completed in reversed(completion_history):
        if completed:
            current_streak += 1
        else:
            break
    return current_streak
