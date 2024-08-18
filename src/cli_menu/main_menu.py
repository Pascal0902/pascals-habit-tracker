import re

from ..habit_tracking.habits import Habit
from ..habit_tracking.users import User
from ..data_storage.interface import StorageInterface
from ..habit_analysis import analytics

from datetime import datetime


def main_menu(data_storage: StorageInterface, user: User):
    while True:
        print(f"--- Welcome, {user.username}! ---")
        print("1: Habit tracking (track habit completion, add habits to tracking)")
        print("2: Habit creation (create new habits and edit existing ones)")
        print("3: Habit analysis (view habit streaks)")
        print("q: Exit program")
        user_selection = input()
        match user_selection:
            case "1":
                habit_tracking_menu(data_storage, user)
            case "2":
                habit_creation_menu(data_storage)
            case "3":
                habit_analysis_menu(user)
            case "q":
                print("Exiting program...")
                break
            case _:
                print("Invalid selection. Please try again.")


def habit_tracking_menu(data_storage: StorageInterface, user: User):
    while True:
        print("--- Habit tracking ---")
        print("1: Track habit completion")
        print("2: Add habit to tracking")
        print("3: Remove habit from tracking")
        print("q: Return to main menu")
        user_selection = input()
        match user_selection:
            case "1":
                track_habit_completion(data_storage, user)
            case "2":
                add_habit_to_tracking(data_storage, user)
            case "3":
                remove_habit_from_tracking(data_storage, user)
            case "q":
                break
            case _:
                print("Invalid selection. Please try again.")


def multi_page_option_selection_menu(selection_name: str, options: list, page_number: int = 0):
    options_on_page = options[page_number * 9:page_number * 9 + 9]
    total_pages = len(options) // 9 + 1
    print(f"--- Please select a {selection_name} ---")
    for i, option in enumerate(options_on_page):
        print(f"{i + 1}: {option}")
    if total_pages > 1:
        print("n: Next page")
        print("p: Previous page")
    print("q: Return to previous menu")
    print(f"Page {page_number + 1} / {total_pages}")
    user_selection = input()
    match user_selection:
        case "n" if len(options) > (page_number + 1) * 9:
            return multi_page_option_selection_menu(selection_name, options, page_number + 1)
        case "n":
            print("No more pages. Please try again.")
            return multi_page_option_selection_menu(selection_name, options, page_number)
        case "p" if page_number > 0:
            return multi_page_option_selection_menu(selection_name, options, page_number - 1)
        case "p":
            print("No previous pages. Please try again.")
            return multi_page_option_selection_menu(selection_name, options, page_number)
        case "q":
            return None
        case _ if user_selection.isdigit():
            selection_index = int(user_selection) - 1
            if selection_index < len(options_on_page):
                return options_on_page[selection_index]
            else:
                print("Invalid selection. Please try again.")
                return multi_page_option_selection_menu(selection_name, options, page_number)
        case _:
            print("Invalid selection. Please try again.")
            return multi_page_option_selection_menu(selection_name, options, page_number)


def track_habit_completion(data_storage: StorageInterface, user: User):
    if len(user.habits) == 0:
        print("No habits to track. Please add a habit to tracking first.")
    else:
        print("--- Track habit completion ---")
        user_habit_names = [userhabit.habit.name for userhabit in user.habits]
        habit_to_track = multi_page_option_selection_menu("habit", user_habit_names)
        if habit_to_track is not None:
            habit_to_track = user.habits[user_habit_names.index(habit_to_track)]
            print(f"Press enter to mark {habit_to_track.habit.name} as completed for today.")
            print("Alternatively, type a date in the format YYYY-MM-DD to mark a different date as completed.")
            user_input = input()
            match user_input:
                case "":
                    habit_to_track.track_completion()
                    print(f"{habit_to_track.habit.name} marked as completed for today.")
                case "q":
                    return
                case _ if re.match(r"^\d{4}-\d{2}-\d{2}$", user_input):
                    completion_time = datetime.strptime(user_input, "%Y-%m-%d")
                    habit_to_track.track_completion(completion_time)
                    print(f"{habit_to_track.habit.name} marked as completed for {completion_time.date()}.")
                case _:
                    print("Invalid input. Please try again.")
                    return track_habit_completion(data_storage, user)


def add_habit_to_tracking(data_storage: StorageInterface, user: User):
    print("--- Add habit to tracking ---")
    all_habit_names = [habit.name for habit in data_storage.get_all_habits()]
    habit_to_add = multi_page_option_selection_menu("habit", all_habit_names)
    if habit_to_add is not None:
        habit_to_add = data_storage.get_habit(habit_to_add)
        user_habit = user.add_habit(habit_to_add)
        data_storage.insert_user_habit(user_habit)
        data_storage.update_user(user)
        print(f"{habit_to_add.name} added to tracking.")


def remove_habit_from_tracking(data_storage: StorageInterface, user: User):
    if len(user.habits) == 0:
        print("No habits to remove from tracking.")
    else:
        print("--- Remove habit from tracking ---")
        user_habit_names = [userhabit.habit.name for userhabit in user.habits]
        habit_to_remove = multi_page_option_selection_menu("habit", user_habit_names)
        if habit_to_remove is not None:
            habit_to_remove = data_storage.get_habit(habit_to_remove)
            removed_userhabit = user.remove_habit(habit_to_remove)
            data_storage.delete_user_habit(removed_userhabit)
            data_storage.update_user(user)
            print(f"{removed_userhabit.habit.name} removed from tracking.")


def habit_creation_menu(data_storage: StorageInterface):
    while True:
        print("--- Habit creation ---")
        print("1: Create new habit")
        print("2: Edit habit task description")
        print("3: Delete existing habit")
        print("q: Return to main menu")
        user_input = input()
        match user_input:
            case "1":
                create_new_habit(data_storage)
            case "2":
                edit_existing_habit(data_storage)
            case "3":
                delete_existing_habit(data_storage)
            case "q":
                break
            case _:
                print("Invalid input. Please try again.")


def create_new_habit(data_storage: StorageInterface):
    print("--- Create new habit ---")
    habit_name = input("Enter habit name: ")
    habit_exists = data_storage.get_habit(habit_name) is not None
    if habit_exists:
        print("Habit with that name already exists. Please try again.")
        return create_new_habit(data_storage)
    else:
        habit_description = input("Enter habit task description: ")
        period = input("Enter habit tracking period (daily, weekly, monthly, quarterly, annually): ")
        while period not in ["daily", "weekly", "monthly", "quarterly", "annually"]:
            print(f"Invalid period {period}. Please try again.")
            period = input("Enter habit tracking period (daily, weekly, monthly, quarterly, annually): ")
        habit = Habit(habit_name, habit_description, period)
        data_storage.insert_habit(habit)
        print(f"{habit_name} created.")


def edit_existing_habit(data_storage: StorageInterface):
    print("--- Edit existing habit ---")
    all_habit_names = [habit.name for habit in data_storage.get_all_habits()]
    habit_to_edit = multi_page_option_selection_menu("habit", all_habit_names)
    if habit_to_edit is not None:
        habit_to_edit = data_storage.get_habit(habit_to_edit)
        print(f"Current task description: {habit_to_edit.task_description}")
        new_task_description = input("Enter new task description: ")
        habit_to_edit.task_description = new_task_description
        data_storage.update_habit(habit_to_edit)
        print(f"{habit_to_edit.name} updated.")


def delete_existing_habit(data_storage: StorageInterface):
    print("--- Delete existing habit ---")
    all_habit_names = [habit.name for habit in data_storage.get_all_habits()]
    habit_to_delete = multi_page_option_selection_menu("habit", all_habit_names)
    if habit_to_delete is not None:
        habit_to_delete = data_storage.get_habit(habit_to_delete)
        no_user_habits = not any(userhabit.habit.name == habit_to_delete.name
                                 for userhabit in data_storage.get_all_user_habits())
        if not no_user_habits:
            data_storage.delete_habit(habit_to_delete)
            print(f"{habit_to_delete.name} deleted.")
        else:
            print(f"{habit_to_delete.name} is currently being tracked by users. "
                  f"Please remove it from tracking before deleting.")


def habit_analysis_menu(user: User):
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
                get_longest_streak_for_specific_habit(user)
            case "6":
                get_longest_all_time_streak_for_specific_habit(user)
            case "q":
                break
            case _:
                print("Invalid input. Please try again.")


def show_all_habits_with_current_streak(user: User):
    print("--- Habits with current streak ---")
    habits_with_streak = analytics.get_all_tracked_habits_with_streak(user)
    if len(habits_with_streak) == 0:
        print("No habits found for user.")
    else:
        for habit, current_streak in habits_with_streak:
            print(f"{habit.name}: {current_streak}")

