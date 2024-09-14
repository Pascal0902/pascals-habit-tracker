import os
import sys

# Get the absolute path of the src directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))

# Add the src directory to sys.path
sys.path.insert(0, src_path)


import datetime
import random

from data_storage.json import JsonStorageInterface
from habit_tracking.users import User

if __name__ == "__main__":
    days_of_data = 30
    completion_rate = 0.75
    username = "testuser"
    storage_file = "demo_data.json"

    storage = JsonStorageInterface(storage_file)
    user = storage.get_user(username)
    if user is None:
        user = User(username)
        storage.insert_user(user)
    all_habits = storage.get_all_habits()
    for habit in all_habits:
        userhabit = user.add_habit(habit)
        userhabit.creation_time = userhabit.creation_time - datetime.timedelta(days=30)
        time_frames = userhabit.habit.get_all_periods_since(userhabit.creation_time)
        for time_frame_start, time_frame_end in time_frames:
            if random.random() < completion_rate:
                time_frame_start = max(time_frame_start, userhabit.creation_time)
                time_frame_end = min(time_frame_end, datetime.datetime.now())
                completion_time = time_frame_start + datetime.timedelta(
                    seconds=random.randint(
                        0, int((time_frame_end - time_frame_start).total_seconds())
                    )
                )
                userhabit.track_completion(completion_time)
        storage.insert_user_habit(userhabit)
    storage.update_user(user)
