from ..data_storage.interface import StorageInterface
from ..habit_tracking.users import User
from .main_menu import main_menu


def user_menu_main(data_storage: StorageInterface):
    print("--- Please select an option ---")
    print("1: Login with existing account")
    print("2: Create a new account")
    print("q: Exit program")
    user_selection = input()
    if user_selection == "1":
        return user_login(data_storage)
    elif user_selection == "2":
        return create_user(data_storage)
    elif user_selection == "q":
        print("Exiting program...")
        return None
    else:
        print("Invalid selection. Please try again.")
        return user_menu_main(data_storage)


def user_login(data_storage: StorageInterface):
    print("--- Please enter your username ---")
    username = input()
    if username == "q":
        return user_menu_main(data_storage)
    user = data_storage.get_user(username)
    if user is None:
        print("User not found. Please try again.")
        return user_login(data_storage)
    return main_menu(data_storage, user)


def create_user(data_storage: StorageInterface):
    print("--- Please enter your username ---")
    username = input()
    if username == "q":
        return user_menu_main(data_storage)
    user = User(username=username, habits=[])
    create_success = data_storage.insert_user(user)
    if create_success:
        return main_menu(data_storage, user)
    else:
        print("Username already exists. Please try again.")
        return create_user(data_storage)
