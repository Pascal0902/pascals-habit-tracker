from cli_menu.habit_analysis_menu import habit_analysis_menu
from cli_menu.habit_creation_menu import habit_creation_menu
from cli_menu.habit_tracking_menu import habit_tracking_menu
from data_storage.interface import StorageInterface
from habit_tracking.users import User


def main_menu(data_storage: StorageInterface, user: User):
    """
    Main cli menu for the application.
    Args:
        data_storage: The data storage to use for the application
        user: The currently logged in user

    Returns:
        None
    """
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
