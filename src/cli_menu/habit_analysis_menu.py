from cli_menu.cli_utils import multi_page_option_selection_menu
from habit_analysis import analytics
from habit_tracking.users import User


def habit_analysis_menu(user: User):
    """
    Menu for habit analysis options.
    Args:
        user: The currently logged in user

    Returns:
        None
    """
    while True:
        print("--- Habit analysis ---")
        print("1: Show all habits with current streak")
        print("2: Show all habits with current streak for specific periodicity")
        print("3: Get habit with all-time longest streak")
        print("4: Get habit with current longest streak")
        print("5: Get longest streak for specific habit")
        print("6: Get longest all-time streak for specific habit")
        print("q: Return to main menu")
        user_input = input()
        match user_input:
            case "1":
                show_all_habits_with_current_streak(user)
            case "2":
                show_all_habits_with_current_streak_for_specific_periodicity(user)
            case "3":
                get_habit_with_all_time_longest_streak(user)
            case "4":
                get_habit_with_current_longest_streak(user)
            case "5":
                get_current_streak_for_specific_habit(user)
            case "6":
                get_longest_all_time_streak_for_specific_habit(user)
            case "q":
                break
            case _:
                print("Invalid input. Please try again.")


def show_all_habits_with_current_streak(user: User):
    """
    Show all habits with current streak for the user.
    Args:
        user: The user to show habits for

    Returns:
        None
    """
    print("--- Habits with current streak ---")
    habits_with_streak = analytics.get_all_tracked_habits_with_streak(user)
    if len(habits_with_streak) == 0:
        print("No habits found for user.")
    else:
        for habit, current_streak in habits_with_streak:
            print(f"{habit.name}: {current_streak}")


def show_all_habits_with_current_streak_for_specific_periodicity(user: User):
    """
    Show all habits with current streak for a specific periodicity.
    Args:
        user: The user to show habits for

    Returns:
        None
    """
    print("--- Habits with current streak for specific periodicity ---")
    period = input("Enter habit tracking period (daily, weekly, monthly, quarterly, annually): ")
    while period not in ["daily", "weekly", "monthly", "quarterly", "annually"]:
        print(f"Invalid period {period}. Please try again.")
        period = input("Enter habit tracking period (daily, weekly, monthly, quarterly, annually): ")
    habits_with_streak = analytics.get_all_tracked_habits_with_streak_for_periodicity(user, period)
    if len(habits_with_streak) == 0:
        print("No habits with this periodicity found for user.")
    else:
        for habit, current_streak in habits_with_streak:
            print(f"{habit.name}: {current_streak}")


def get_habit_with_all_time_longest_streak(user: User):
    """
    Get the habit with the all-time longest streak for the user.
    Args:
        user: The user to get the longest habit streak for

    Returns:
        None
    """
    print("--- Habit with all-time longest streak ---")
    habit, longest_streak = analytics.get_all_time_longest_habit_streak(user)
    if habit is not None:
        print(f"{habit.name}: {longest_streak}")
    else:
        print("No habits found for user.")


def get_habit_with_current_longest_streak(user: User):
    """
    Get the habit with the current longest streak for the user.
    Args:
        user: The user to get the longest current habit streak for

    Returns:
        None
    """
    print("--- Habit with current longest streak ---")
    habit, longest_streak = analytics.get_current_longest_habit_streak(user)
    if habit is not None:
        print(f"{habit.name}: {longest_streak}")
    else:
        print("No habits found for user.")


def get_current_streak_for_specific_habit(user: User):
    """
    Get the current streak for a specific habit.
    Args:
        user: The user to get the streak for

    Returns:
        None
    """
    print("--- Longest streak for specific habit ---")
    all_habit_names = [userhabit.habit.name for userhabit in user.habits]
    habit_name = multi_page_option_selection_menu("habit", all_habit_names)
    if habit_name is not None:
        userhabit = next(userhabit for userhabit in user.habits if userhabit.habit.name == habit_name)
        streak = analytics.get_current_streak_for_habit(userhabit)
        print(f"{habit_name}: {streak}")


def get_longest_all_time_streak_for_specific_habit(user: User):
    """
    Get the longest all-time streak for a specific habit.
    Args:
        user: The user to get the streak for

    Returns:
        None
    """
    print("--- Longest all-time streak for specific habit ---")
    all_habit_names = [userhabit.habit.name for userhabit in user.habits]
    habit_name = multi_page_option_selection_menu("habit", all_habit_names)
    if habit_name is not None:
        userhabit = next(userhabit for userhabit in user.habits if userhabit.habit.name == habit_name)
        longest_streak = analytics.get_longest_streak_for_habit(userhabit)
        print(f"{habit_name}: {longest_streak}")