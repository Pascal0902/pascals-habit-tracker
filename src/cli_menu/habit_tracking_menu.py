import re
from datetime import datetime

from cli_menu.cli_utils import multi_page_option_selection_menu
from data_storage.interface import StorageInterface
from habit_tracking.users import User


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
                    data_storage.update_user_habit(habit_to_track)
                case "q":
                    return
                case _ if re.match(r"^\d{4}-\d{2}-\d{2}$", user_input):
                    completion_time = datetime.strptime(user_input, "%Y-%m-%d")
                    if completion_time > datetime.now():
                        print("Cannot mark a habit as completed for a future date. Please try again.")
                        return track_habit_completion(data_storage, user)
                    elif completion_time < habit_to_track.creation_time:
                        print("Cannot mark a habit as completed before the habit was started. Please try again.")
                        return track_habit_completion(data_storage, user)
                    else:
                        habit_to_track.track_completion(completion_time)
                        print(f"{habit_to_track.habit.name} marked as completed for {completion_time.date()}.")
                        data_storage.update_user_habit(habit_to_track)
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