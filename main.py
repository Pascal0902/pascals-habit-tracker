import os
import sys

# Get the absolute path of the src directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))

# Add the src directory to sys.path
sys.path.insert(0, src_path)


from cli_menu.user_selection import user_menu_main
from data_storage.json import JsonStorageInterface

if __name__ == "__main__":
    storage = JsonStorageInterface("demo_data.json")
    user_menu_main(storage)
