from abc import ABC, abstractmethod

from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


class StorageInterface(ABC):
    """
    An interface for interacting with a data storage system.
    """

    @abstractmethod
    def insert_user(self, user: User) -> bool:
        """
        Insert a new user into the data storage.
        Args:
            user: The User object to insert into the data storage.

        Returns:
            True if the user was successfully inserted, False otherwise.
        """
        pass

    @abstractmethod
    def update_user(self, user: User) -> bool:
        """
        Update an existing user in the data storage.
        Args:
            user: The User object to update in the data storage.

        Returns:
            True if the user was successfully updated, False otherwise.
        """
        pass

    @abstractmethod
    def delete_user(self, user: User) -> bool:
        """
        Delete an existing user from the data storage.
        Args:
            user: The User object to delete from the data storage.

        Returns:
            True if the user was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def get_user(self, username: str) -> User | None:
        """
        Retrieve a user from the data storage by their username.
        Args:
            username: The username of the user to retrieve.

        Returns:
            The User object corresponding to the provided username, or None if the user does not exist.
        """
        pass

    @abstractmethod
    def insert_habit(self, habit: Habit) -> bool:
        """
        Insert a new habit into the data storage.
        Args:
            habit: The Habit object to insert into the data storage.

        Returns:
            True if the habit was successfully inserted, False otherwise.
        """
        pass

    @abstractmethod
    def update_habit(self, habit: Habit) -> bool:
        """
        Update an existing habit in the data storage.
        Args:
            habit: The Habit object to update in the data storage.

        Returns:
            True if the habit was successfully updated, False otherwise.
        """
        pass

    @abstractmethod
    def delete_habit(self, habit: Habit) -> bool:
        """
        Delete an existing habit from the data storage.
        Args:
            habit: The Habit object to delete from the data storage.

        Returns:
            True if the habit was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def get_habit(self, name: str) -> Habit | None:
        """
        Retrieve a habit from the data storage by its name.
        Args:
            name: The name of the habit to retrieve.

        Returns:
            The Habit object corresponding to the provided name, or None if the habit does not exist.
        """
        pass

    @abstractmethod
    def get_all_habits(self) -> list[Habit]:
        """
        Retrieve all habits from the data storage.
        Returns:
            A list of all Habit objects in the data storage.
        """
        pass

    @abstractmethod
    def insert_user_habit(self, user_habit: UserHabit) -> bool:
        """
        Insert a new UserHabit object into the data storage.
        Args:
            user_habit: The UserHabit object to insert into the data storage.

        Returns:
            True if the UserHabit object was successfully inserted, False otherwise.
        """
        pass

    @abstractmethod
    def update_user_habit(self, user_habit: UserHabit) -> bool:
        """
        Update an existing UserHabit object in the data storage.
        Args:
            user_habit: The UserHabit object to update in the data storage.

        Returns:
            True if the UserHabit object was successfully updated, False otherwise.
        """
        pass

    @abstractmethod
    def delete_user_habit(self, user_habit: UserHabit) -> bool:
        """
        Delete an existing UserHabit object from the data storage.
        Args:
            user_habit: The UserHabit object to delete from the data storage.

        Returns:
            True if the UserHabit object was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def get_user_habit(self, userhabit_id: str) -> UserHabit | None:
        """
        Retrieve a UserHabit object from the data storage by its ID.
        Args:
            userhabit_id: The ID of the UserHabit object to retrieve.

        Returns:
            The UserHabit object corresponding to the provided ID, or None if the UserHabit object does not exist.
        """
        pass

    @abstractmethod
    def get_all_user_habits(self) -> list[UserHabit]:
        """
        Retrieve all UserHabit objects from the data storage.
        Returns:
            A list of all UserHabit objects in the data storage.
        """
        pass
