from cli_menu.cli_utils import multi_page_option_selection_menu
from data_storage.interface import StorageInterface
from habit_tracking.habits import Habit


def habit_creation_menu(data_storage: StorageInterface):
    """
    Menu for creating, editing, and deleting habits.
    Args:
        data_storage: The data storage to use for the application

    Returns:
        None
    """
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
    """
    Create a new habit.
    Args:
        data_storage: The data storage to use for the application

    Returns:
        None
    """
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
    """
    Edit an existing habit.
    Args:
        data_storage: The data storage to use for the application

    Returns:
        None
    """
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
    """
    Delete an existing habit.
    Args:
        data_storage: The data storage to use for the application

    Returns:
        None
    """
    print("--- Delete existing habit ---")
    all_habit_names = [habit.name for habit in data_storage.get_all_habits()]
    habit_to_delete = multi_page_option_selection_menu("habit", all_habit_names)
    if habit_to_delete is not None:
        habit_to_delete = data_storage.get_habit(habit_to_delete)
        no_user_habits = not any(userhabit.habit.name == habit_to_delete.name
                                 for userhabit in data_storage.get_all_user_habits())
        if no_user_habits:
            data_storage.delete_habit(habit_to_delete)
            print(f"{habit_to_delete.name} deleted.")
        else:
            print(f"{habit_to_delete.name} is currently being tracked by users. "
                  f"Please remove it from tracking before deleting.")