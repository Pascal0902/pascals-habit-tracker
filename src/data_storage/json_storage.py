
import json
from typing import Any
from pathlib import Path

from src.data_storage.interface import StorageInterface
from src.habit_tracking.habits import Habit, UserHabit
from src.habit_tracking.users import User


class JsonStorage(StorageInterface):
    """
    A JSON-file based implementation of the StorageInterface.
    This class stores and retrieves User, Habit, and UserHabit objects
    from a JSON file.
    """

    def __init__(self, storage_file: str = "data.json"):
        self.storage_file = Path(storage_file)
        self._initialize_storage_file()

    def _initialize_storage_file(self):
        """
        Initializes the JSON storage file with empty lists if it doesn't exist.
        """
        if not self.storage_file.exists():
            self._write_data({"users": [], "habits": [], "user_habits": []})

    def _read_data(self) -> dict[str, Any]:
        """
        Reads all data from the JSON storage file.
        Returns:
            A dictionary containing all stored data.
        """
        with open(self.storage_file, "r") as f:
            return json.load(f)

    def _write_data(self, data: dict[str, Any]):
        """
        Writes data to the JSON storage file.
        Args:
            data: The dictionary containing data to write.
        """
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def insert_user(self, user: User) -> bool:
        data = self._read_data()
        if any(u["username"] == user.username for u in data["users"]):
            return False  # User already exists
        data["users"].append(user.to_dict())
        self._write_data(data)
        return True

    def update_user(self, user: User) -> bool:
        data = self._read_data()
        for i, u in enumerate(data["users"]):
            if u["username"] == user.username:
                data["users"][i] = user.to_dict()
                self._write_data(data)
                return True
        return False

    def delete_user(self, user: User) -> bool:
        data = self._read_data()
        initial_len = len(data["users"])
        data["users"] = [u for u in data["users"] if u["username"] != user.username]
        if len(data["users"]) < initial_len:
            self._write_data(data)
            return True
        return False

    def get_user(self, username: str) -> User | None:
        data = self._read_data()
        all_user_habits = self.get_all_user_habits()
        for u in data["users"]:
            if u["username"] == username:
                return User.from_dict(u, all_user_habits=all_user_habits)
        return None

    def insert_habit(self, habit: Habit) -> bool:
        data = self._read_data()
        if any(h["name"] == habit.name for h in data["habits"]):
            return False
        data["habits"].append(habit.to_dict())
        self._write_data(data)
        return True

    def update_habit(self, habit: Habit) -> bool:
        data = self._read_data()
        for i, h in enumerate(data["habits"]):
            if h["name"] == habit.name:
                data["habits"][i] = habit.to_dict()
                self._write_data(data)
                return True
        return False

    def delete_habit(self, habit: Habit) -> bool:
        data = self._read_data()
        initial_len = len(data["habits"])
        data["habits"] = [h for h in data["habits"] if h["name"] != habit.name]
        if len(data["habits"]) < initial_len:
            self._write_data(data)
            return True
        return False

    def get_habit(self, name: str) -> Habit | None:
        data = self._read_data()
        for h in data["habits"]:
            if h["name"] == name:
                return Habit.from_dict(h)
        return None

    def get_all_habits(self) -> list[Habit]:
        data = self._read_data()
        return [Habit.from_dict(h) for h in data["habits"]]

    def insert_user_habit(self, user_habit: UserHabit) -> bool:
        data = self._read_data()
        if any(uh["userhabit_id"] == user_habit.userhabit_id for uh in data["user_habits"]):
            return False
        data["user_habits"].append(user_habit.to_dict())
        self._write_data(data)
        return True

    def update_user_habit(self, user_habit: UserHabit) -> bool:
        data = self._read_data()
        for i, uh in enumerate(data["user_habits"]):
            if uh["userhabit_id"] == user_habit.userhabit_id:
                data["user_habits"][i] = user_habit.to_dict()
                self._write_data(data)
                return True
        return False

    def delete_user_habit(self, user_habit: UserHabit) -> bool:
        data = self._read_data()
        initial_len = len(data["user_habits"])
        data["user_habits"] = [uh for uh in data["user_habits"] if uh["userhabit_id"] != user_habit.userhabit_id]
        if len(data["user_habits"]) < initial_len:
            self._write_data(data)
            return True
        return False

    def get_user_habit(self, userhabit_id: str) -> UserHabit | None:
        data = self._read_data()
        all_habits = self.get_all_habits()
        for uh in data["user_habits"]:
            if uh["userhabit_id"] == userhabit_id:
                return UserHabit.from_dict(uh, all_habits=all_habits)
        return None

    def get_all_user_habits(self) -> list[UserHabit]:
        data = self._read_data()
        all_habits = self.get_all_habits()
        return [UserHabit.from_dict(uh, all_habits=all_habits) for uh in data["user_habits"] if UserHabit.from_dict(uh, all_habits=all_habits) is not None]

