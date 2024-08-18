import json
import os
from datetime import datetime

from .interface import StorageInterface
from ..habit_tracking.users import User
from ..habit_tracking.habits import Habit, UserHabit


class JsonStorageInterface(StorageInterface):
    """
    A data storage interface that uses JSON files to store data.
    """
    def __init__(self, file_path: str):
        """
        Args:
            file_path: The path to the JSON file to use for data storage.
        """
        assert file_path.endswith('.json'), "File path must be a JSON file."
        self.file_path = file_path
        self.data = self.__load_json()

    def __load_json(self) -> dict:
        """
        Load the JSON data from the file.
        Returns:
            The JSON data loaded from the file, or the basic data structure dictionary if the file does not exist.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as fp:
                return json.load(fp)
        else:
            return {
                "users": {},
                "habits": {},
                "user_habits": {}
            }

    def __save_json(self):
        """
        Save the JSON data to the file.
        Returns:
            None
        """
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w') as fp:
            json.dump(self.data, fp)

    def insert_user(self, user: User) -> bool:
        """
        Insert a new user into the data storage.
        Args:
            user: The User object to insert into the data storage.

        Returns:
            True if the user was successfully inserted, False otherwise.
        """
        if user.username in self.data['users']:
            return False
        self.data['users'][user.username] = user.json()
        self.__save_json()
        return True

    def update_user(self, user: User) -> bool:
        """
        Update an existing user in the data storage.
        Args:
            user: The User object to update in the data storage.

        Returns:
            True if the user was successfully updated, False otherwise.
        """
        if user.username not in self.data['users']:
            return False
        self.data['users'][user.username] = user.json()
        self.__save_json()
        return True

    def delete_user(self, user: User) -> bool:
        """
        Delete an existing user from the data storage.
        Args:
            user: The User object to delete from the data storage.

        Returns:
            True if the user was successfully deleted, False otherwise.
        """
        if user.username not in self.data['users']:
            return False
        del self.data['users'][user.username]
        self.__save_json()
        return True

    def get_user(self, username: str) -> User | None:
        """
        Retrieve a user from the data storage by their username.
        Args:
            username: The username of the user to retrieve.

        Returns:
            The User object corresponding to the provided username, or None if the user does not exist.
        """
        if username not in self.data['users']:
            return None
        user_data = self.data['users'][username]
        initialised_user_habits = [self.get_user_habit(user_habit_id) for user_habit_id in user_data['user_habits']]
        return User(username=user_data["username"], habits=initialised_user_habits)

    def insert_habit(self, habit: Habit) -> bool:
        """
        Insert a new habit into the data storage.
        Args:
            habit: The Habit object to insert into the data storage.

        Returns:
            True if the habit was successfully inserted, False otherwise.
        """
        if habit.name in self.data['habits']:
            return False
        self.data['habits'][habit.name] = habit.json()
        self.__save_json()
        return True

    def update_habit(self, habit: Habit) -> bool:
        """
        Update an existing habit in the data storage.
        Args:
            habit: The Habit object to update in the data storage.

        Returns:
            True if the habit was successfully updated, False otherwise.
        """
        if habit.name not in self.data['habits']:
            return False
        self.data['habits'][habit.name] = habit.json()
        self.__save_json()
        return True

    def delete_habit(self, habit: Habit) -> bool:
        """
        Delete an existing habit from the data storage.
        Args:
            habit: The Habit object to delete from the data storage.

        Returns:
            True if the habit was successfully deleted, False otherwise.
        """
        if habit.name not in self.data['habits']:
            return False
        del self.data['habits'][habit.name]
        self.__save_json()
        return True

    def get_habit(self, habit_name: str) -> Habit | None:
        """
        Retrieve a habit from the data storage by its name.
        Args:
            name: The name of the habit to retrieve.

        Returns:
            The Habit object corresponding to the provided name, or None if the habit does not exist.
        """
        if habit_name not in self.data['habits']:
            return None
        habit_data = self.data['habits'][habit_name]
        creation_time = datetime.fromisoformat(habit_data["creation_time"])
        return Habit(name=habit_data["name"], task_description=habit_data["task_description"],
                     period=habit_data["period"], creation_time=creation_time)

    def get_all_habits(self) -> list[Habit]:
        """
        Retrieve all habits from the data storage.
        Returns:
            A list of all Habit objects in the data storage.
        """
        habits = []
        for habit_data in self.data['habits'].values():
            creation_time = datetime.fromisoformat(habit_data["creation_time"])
            habits.append(Habit(name=habit_data["name"], task_description=habit_data["task_description"],
                                period=habit_data["period"], creation_time=creation_time))
        return habits

    def insert_user_habit(self, user_habit: UserHabit) -> bool:
        """
        Insert a new UserHabit object into the data storage.
        Args:
            user_habit: The UserHabit object to insert into the data storage.

        Returns:
            True if the UserHabit object was successfully inserted, False otherwise.
        """
        if user_habit.userhabit_id in self.data['user_habits']:
            return False
        self.data['user_habits'][user_habit.userhabit_id] = user_habit.json()
        self.__save_json()
        return True

    def update_user_habit(self, user_habit: UserHabit) -> bool:
        """
        Update an existing UserHabit object in the data storage.
        Args:
            user_habit: The UserHabit object to update in the data storage.

        Returns:
            True if the UserHabit object was successfully updated, False otherwise.
        """
        if user_habit.userhabit_id not in self.data['user_habits']:
            return False
        self.data['user_habits'][user_habit.userhabit_id] = user_habit.json()
        self.__save_json()
        return True

    def delete_user_habit(self, user_habit: UserHabit) -> bool:
        """
        Delete an existing UserHabit object from the data storage.
        Args:
            user_habit: The UserHabit object to delete from the data storage.

        Returns:
            True if the UserHabit object was successfully deleted, False otherwise.
        """
        if user_habit.userhabit_id not in self.data['user_habits']:
            return False
        del self.data['user_habits'][user_habit.userhabit_id]
        self.__save_json()
        return True

    def get_user_habit(self, user_habit_id: str) -> UserHabit | None:
        """
        Retrieve a UserHabit object from the data storage by its ID.
        Args:
            userhabit_id: The ID of the UserHabit object to retrieve.

        Returns:
            The UserHabit object corresponding to the provided ID, or None if the UserHabit object does not exist.
        """
        if user_habit_id not in self.data['user_habits']:
            return None
        user_habit_data = self.data['user_habits'][user_habit_id]
        habit = self.get_habit(user_habit_data["habit"])
        completion_times = [datetime.fromisoformat(completion_time)
                            for completion_time in user_habit_data["completion_times"]]
        creation_time = datetime.fromisoformat(user_habit_data["creation_time"])
        return UserHabit(userhabit_id=user_habit_data["userhabit_id"], habit=habit, completion_times=completion_times,
                         creation_time=creation_time)

    def get_all_user_habits(self) -> list[UserHabit]:
        """
        Retrieve all UserHabit objects from the data storage.
        Returns:
            A list of all UserHabit objects in the data storage.
        """
        user_habits = []
        for user_habit_data in self.data['user_habits'].values():
            habit = self.get_habit(user_habit_data["habit"])
            completion_times = [datetime.fromisoformat(completion_time)
                                for completion_time in user_habit_data["completion_times"]]
            creation_time = datetime.fromisoformat(user_habit_data["creation_time"])
            user_habits.append(UserHabit(userhabit_id=user_habit_data["userhabit_id"], habit=habit,
                                         completion_times=completion_times, creation_time=creation_time))
        return user_habits
