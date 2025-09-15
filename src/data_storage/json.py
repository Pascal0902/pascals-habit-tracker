import json
import os
from datetime import datetime
from typing import Dict, List

from data_storage.interface import StorageInterface
from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


class JsonStorageInterface(StorageInterface):
    """
    A JSON file-based implementation of the StorageInterface.
    
    This class provides data persistence using JSON files, storing users, habits,
    and user habits in a structured format.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the JSON storage interface.
        
        Args:
            file_path: Path to the JSON file for data storage. Must end with .json
        """
        assert file_path.endswith('.json'), "File path must end with .json"
        self.file_path = file_path
        self._load_data()
    
    def _load_data(self):
        """Load data from JSON file or initialize empty data structure."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {
                'users': {},
                'habits': {},
                'user_habits': {}
            }
        
        self.data = data
    
    def _save_data(self):
        """Save current data to JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def _user_from_dict(self, user_data: Dict) -> User:
        """Create User object from dictionary data."""
        user = User(username=user_data['username'])
        # Load user habits
        for userhabit_id in user_data['habits']:
            if userhabit_id in self.data['user_habits']:
                user_habit = self._userhabit_from_dict(self.data['user_habits'][userhabit_id])
                user.habits.append(user_habit)
        return user
    
    def _habit_from_dict(self, habit_data: Dict) -> Habit:
        """Create Habit object from dictionary data."""
        creation_time = datetime.fromisoformat(habit_data['creation_time'])
        return Habit(
            name=habit_data['name'],
            task_description=habit_data['task_description'],
            period=habit_data['period'],
            creation_time=creation_time
        )
    
    def _userhabit_from_dict(self, userhabit_data: Dict) -> UserHabit:
        """Create UserHabit object from dictionary data."""
        habit = self.get_habit(userhabit_data['habit'])
        if habit is None:
            raise ValueError(f"Habit {userhabit_data['habit']} not found")
        
        completion_times = [datetime.fromisoformat(time_str) for time_str in userhabit_data['completion_times']]
        creation_time = datetime.fromisoformat(userhabit_data['creation_time'])
        
        return UserHabit(
            habit=habit,
            userhabit_id=userhabit_data['userhabit_id'],
            completion_times=completion_times,
            creation_time=creation_time
        )
    
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
        self._save_data()
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
        self._save_data()
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
        self._save_data()
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
        
        return self._user_from_dict(self.data['users'][username])
    
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
        self._save_data()
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
        self._save_data()
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
        self._save_data()
        return True
    
    def get_habit(self, name: str) -> Habit | None:
        """
        Retrieve a habit from the data storage by its name.
        
        Args:
            name: The name of the habit to retrieve.
        
        Returns:
            The Habit object corresponding to the provided name, or None if the habit does not exist.
        """
        if name not in self.data['habits']:
            return None
        
        return self._habit_from_dict(self.data['habits'][name])
    
    def get_all_habits(self) -> list[Habit]:
        """
        Retrieve all habits from the data storage.
        
        Returns:
            A list of all Habit objects in the data storage.
        """
        return [self._habit_from_dict(habit_data) for habit_data in self.data['habits'].values()]
    
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
        self._save_data()
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
        self._save_data()
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
        self._save_data()
        return True
    
    def get_user_habit(self, userhabit_id: str) -> UserHabit | None:
        """
        Retrieve a UserHabit object from the data storage by its ID.
        
        Args:
            userhabit_id: The ID of the UserHabit object to retrieve.
        
        Returns:
            The UserHabit object corresponding to the provided ID, or None if the UserHabit object does not exist.
        """
        if userhabit_id not in self.data['user_habits']:
            return None
        
        return self._userhabit_from_dict(self.data['user_habits'][userhabit_id])
    
    def get_all_user_habits(self) -> list[UserHabit]:
        """
        Retrieve all UserHabit objects from the data storage.
        
        Returns:
            A list of all UserHabit objects in the data storage.
        """
        user_habits = []
        for userhabit_data in self.data['user_habits'].values():
            user_habits.append(self._userhabit_from_dict(userhabit_data))
        return user_habits