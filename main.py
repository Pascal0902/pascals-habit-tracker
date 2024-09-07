from cli_menu.user_selection import user_menu_main
from data_storage.json import JsonStorageInterface


if __name__ == "__main__":
    storage = JsonStorageInterface("demo_data.json")
    user_menu_main(storage)
