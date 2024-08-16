from .habits import UserHabit, Habit


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
        self.habits = habits if habits is not None else []

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

    def add_habit(self, habit: Habit):
        """
        Add a new habit to the user's list of tracked habits. Each habit can only be tracked once by a user.
        If the habit is already being tracked, a ValueError is raised.
        Args:
            habit: The Habit object to add to the user's list of tracked habits.

        Returns:
            None
        """
        if self.get_userhabit_for_habit(habit) is None:
            self.habits.append(UserHabit(habit=habit))
        else:
            raise ValueError(f"Habit {habit.name} already exists for user {self.username}")

    def remove_habit(self, habit: Habit):
        """
        Remove a habit from the user's list of tracked habits.
        If the habit is not being tracked, a ValueError is raised.
        Args:
            habit: The Habit object to remove from the user's list of tracked habits.

        Returns:
            None
        """
        user_habit = self.get_userhabit_for_habit(habit)
        if user_habit is not None:
            self.habits.remove(user_habit)
        else:
            raise ValueError(f"Habit {habit.name} does not exist for user {self.username}")
