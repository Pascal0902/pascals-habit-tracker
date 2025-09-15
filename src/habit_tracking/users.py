from habit_tracking.habits import Habit, UserHabit


class User:
    """
    A class to represent a user within the habit tracking app.
    """

    def __init__(self, username: str, habits: list[UserHabit] = None):
        """
        Args:
            username: The username of the user. Must be unique, since this value acts as the primary key.
            habits: A list of UserHabit objects representing the habits the user is tracking. Defaults to an empty list.
        """
        self.username = username
        # Ensure that the habits list only contains unique UserHabit objects based on their userhabit_id
        self.habits = []
        if habits is not None:
            seen_ids = set()
            for user_habit in habits:
                if user_habit.userhabit_id not in seen_ids:
                    self.habits.append(user_habit)
                    seen_ids.add(user_habit.userhabit_id)



    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.username == other.username

    def __hash__(self):
        return hash(self.username)


    def get_userhabit_for_habit(self, habit: Habit) -> UserHabit | None:
        """
        Get the UserHabit object associated with a given Habit object.
        Args:
            habit: The Habit object to search for in the user's habits.

        Returns:
            The UserHabit object associated with the given Habit, or None if the habit is not tracked by the user.
        """
        for user_habit in self.habits:
            if user_habit.habit.name == habit.name:
                return user_habit
        return None

    def add_habit(self, habit: Habit) -> UserHabit:
        """
        Add a new habit to the user's list of tracked habits. Each habit can only be tracked once by a user.
        If the habit is already being tracked, a ValueError is raised.
        Args:
            habit: The Habit object to add to the user's list of tracked habits.

        Returns:
            UserHabit object used for tracking the habit for the user.
        """
        if self.get_userhabit_for_habit(habit) is None:
            user_habit = UserHabit(habit=habit)
            self.habits.append(user_habit)
            return user_habit
        else:
            raise ValueError(
                f"Habit {habit.name} already exists for user {self.username}"
            )

    def get_user_habit(self, userhabit_id: str) -> UserHabit | None:
        """
        Get a UserHabit object by its userhabit_id.
        Args:
            userhabit_id: The ID of the UserHabit object to retrieve.
        Returns:
            The UserHabit object with the matching ID, or None if not found.
        """
        for user_habit in self.habits:
            if user_habit.userhabit_id == userhabit_id:
                return user_habit
        return None

    def update_user_habit(self, updated_user_habit: UserHabit) -> bool:
        """
        Update an existing UserHabit object in the user's list.
        Args:
            updated_user_habit: The UserHabit object with updated information.
        Returns:
            True if the UserHabit was updated, False otherwise.
        """
        for i, user_habit in enumerate(self.habits):
            if user_habit.userhabit_id == updated_user_habit.userhabit_id:
                self.habits[i] = updated_user_habit
                return True
        return False

    def delete_user_habit(self, userhabit_id: str) -> bool:
        """
        Delete a UserHabit object from the user's list by its ID.
        Args:
            userhabit_id: The ID of the UserHabit to delete.
        Returns:
            True if the UserHabit was deleted, False otherwise.
        """
        initial_len = len(self.habits)
        self.habits = [uh for uh in self.habits if uh.userhabit_id != userhabit_id]
        return len(self.habits) < initial_len

    def remove_habit(self, habit: Habit) -> UserHabit:
        """
        Remove a habit from the user's list of tracked habits.
        If the habit is not being tracked, a ValueError is raised.
        Args:
            habit: The Habit object to remove from the user's list of tracked habits.

        Returns:
            UserHabit object that was removed from the user's list of tracked habits.
        """
        user_habit = self.get_userhabit_for_habit(habit)
        if user_habit is not None:
            self.habits.remove(user_habit)
            return user_habit
        else:
            raise ValueError(
                f"Habit {habit.name} does not exist for user {self.username}"
            )

    def json(self):
        """
        Returns all values of the object in a json compatible format for easier storage
        Returns:
            All value of the object in a json compatible format
        """
        return {
            "username": self.username,
            "habits": [user_habit.userhabit_id for user_habit in self.habits],
        }
