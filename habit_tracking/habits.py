import uuid
from datetime import datetime, timedelta


class Habit:
    """
    A class to represent a habit within the habit tracking app.
    """
    def __init__(self, name: str, task_description: str, period: str, creation_time: datetime = None):
        """
        Args:
            name: The name of the habit. Must be unique, since this value acts as the primary key.
            task_description: A description of the task to be completed as part of this habit.
            period: The period over which the habit should be completed (daily, weekly, monthly, quarterly, annually).
            creation_time: The time at which the habit was created. Defaults to the current time.
        """
        self.name = name
        self.task_description = task_description
        assert period in ['daily', 'weekly', 'monthly', 'quarterly', 'annually'], "Unsupported period type provided."
        self.period = period
        self.creation_time = creation_time if creation_time is not None else datetime.now()

    def get_period_start_end(self, target_time: datetime) -> tuple[datetime, datetime]:
        """
        Get the start and end times for the period in which the target time falls.
        Args:
            target_time: The target time for which to determine the period start and end times.

        Returns:
            A tuple containing the start and end times for the period in which the target time falls.
        """
        match self.period:
            case 'daily':
                start = datetime(target_time.year, target_time.month, target_time.day)
                end = start + timedelta(days=1)
            case 'weekly':
                start = target_time - timedelta(days=target_time.weekday())
                end = start + timedelta(days=7)
            case 'monthly':
                start = datetime(target_time.year, target_time.month, 1)
                if target_time.month == 12:
                    end = datetime(target_time.year + 1, 1, 1)
                else:
                    end = datetime(target_time.year, target_time.month + 1, 1)
            case 'quarterly':
                quarter_start_month = ((target_time.month - 1) // 3) * 3 + 1
                start = datetime(target_time.year, quarter_start_month, 1)
                if quarter_start_month == 10:
                    end = datetime(target_time.year + 1, 1, 1)
                else:
                    end = datetime(target_time.year, quarter_start_month + 3, 1)
            case 'annually':
                start = datetime(target_time.year, 1, 1)
                end = datetime(target_time.year + 1, 1, 1)
            case _:
                raise ValueError("Unsupported period type registered in habit (this should never happen).")
        return start, end

    def get_next_period(self, period_end: datetime) -> tuple[datetime, datetime]:
        """
        Get the start and end times for the period immediately following the period ending at the provided time.
        Args:
            period_end: The end time of the period for which to determine the next period.

        Returns:
            A tuple containing the start and end times for the period immediately following the provided period.
        """
        match self.period:
            case 'daily':
                next_start = period_end
                next_end = next_start + timedelta(days=1)
            case 'weekly':
                next_start = period_end
                next_end = next_start + timedelta(days=7)
            case 'monthly':
                next_start = period_end
                if period_end.month == 12:
                    next_end = datetime(period_end.year + 1, 1, 1)
                else:
                    next_end = datetime(period_end.year, period_end.month + 1, 1)
            case 'quarterly':
                next_start = period_end
                quarter_start_month = ((period_end.month - 1) // 3) * 3 + 1
                if quarter_start_month == 10:
                    next_end = datetime(period_end.year + 1, 1, 1)
                else:
                    next_end = datetime(period_end.year, quarter_start_month + 3, 1)
            case 'annually':
                next_start = period_end
                next_end = datetime(period_end.year + 1, 1, 1)
            case _:
                raise ValueError("Unsupported period type registered in habit (this should never happen).")
        return next_start, next_end

    def get_all_periods_since(self, start_time: datetime) -> list[tuple[datetime, datetime]]:
        """
        Get a list of all periods that have occurred since the provided start time.
        Args:
            start_time: The time from which to start generating periods.

        Returns:
            A list of tuples, each containing the start and end times for a period that has occurred since the start time.
        """
        periods = []
        current_period_start, current_period_end = self.get_period_start_end(start_time)
        while current_period_start < datetime.now():
            periods.append((current_period_start, current_period_end))
            current_period_start, current_period_end = self.get_next_period(current_period_end)
        return periods


class UserHabit:
    """
    A class to represent a habit being tracked by a user within the habit tracking app.
    """
    def __init__(self, habit: Habit, userhabit_id: str = None, completion_times: list[datetime] = None,
                 creation_time: datetime = None):
        """
        Args:
            habit: The Habit object to be tracked by the user.
            userhabit_id: A unique identifier for the UserHabit object. If not provided, a random UUID is generated.
            completion_times: A list of datetime objects representing the times at which the habit was completed.
            creation_time: The time at which the UserHabit object was created. Defaults to the current time.
        """
        self.habit = habit
        self.userhabit_id = userhabit_id if userhabit_id is not None else uuid.uuid4().hex
        self.completion_times = completion_times if completion_times is not None else []
        self.creation_time = creation_time if creation_time is not None else datetime.now()

    def period_completed(self, period_start: datetime, period_end: datetime) -> bool:
        """
        Check if the habit has been completed within the provided period.
        Args:
            period_start: The start time of the period to check.
            period_end: The end time of the period to check.

        Returns:
            True if the habit has been completed within the period, False otherwise.
        """
        return any([period_start <= completion_time < period_end for completion_time in self.completion_times])

    def track_completion(self, completion_time: datetime = None) -> bool:
        """
        Track a completion of the habit at the provided time.
        Args:
            completion_time: The time at which the habit was completed. If not provided, the current time is used.

        Returns:
            True if the completion was successfully tracked, False if the habit was already completed for the period.
        """
        completion_time = completion_time if completion_time is not None else datetime.now()
        period_start, period_end = self.habit.get_period_start_end(completion_time)
        if not self.period_completed(period_start, period_end):
            self.completion_times.append(completion_time)
            return True
        else:
            return False

    def get_completion_history(self) -> list[tuple[datetime, datetime, bool]]:
        """
        Get the completion history of the habit, including periods and whether the habit was completed in each period.
        Returns:
            A list of tuples, each containing the start and end times of a period, and a boolean indicating whether the
            habit was completed in that period.
        """
        all_periods_since_creation = self.habit.get_all_periods_since(self.creation_time)
        return [(period_start, period_end, self.period_completed(period_start, period_end))
                for period_start, period_end in all_periods_since_creation]
