#!/usr/bin/env python3
"""
Demo Data Creation Script for Pascal's Habit Tracker

This script creates realistic demo data for testing the habit tracker application.
It generates users with various habits and realistic completion patterns over
a configurable time period.

Usage:
    python create_demo_data.py

Configuration can be adjusted by modifying the parameters in the main section.
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Get the absolute path of the src directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))

# Add the src directory to sys.path
sys.path.insert(0, src_path)

from data_storage.json import JsonStorageInterface
from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


def create_realistic_habits():
    """
    Create a collection of realistic habits with various periodicities.
    
    Returns:
        List[Habit]: A list of realistic habit objects
    """
    habits_data = [
        # Daily habits
        ("Morning Exercise", "Exercise for 30 minutes every morning to boost energy and stay healthy", "daily"),
        ("Drink Water", "Drink at least 8 glasses of water throughout the day", "daily"),
        ("Read for 30 Minutes", "Read books, articles, or educational content for personal growth", "daily"),
        ("Take Vitamins", "Take daily vitamin supplements as recommended by your healthcare provider", "daily"),
        ("Practice Gratitude", "Write down three things you're grateful for each day", "daily"),
        ("Meditate", "Practice mindfulness meditation for 10-15 minutes", "daily"),
        ("Review Daily Goals", "Review and plan your daily objectives and priorities", "daily"),
        
        # Weekly habits
        ("Meal Planning", "Plan your meals for the week to eat better and save time", "weekly"),
        ("Grocery Shopping", "Buy groceries for the week and stick to your shopping list", "weekly"),
        ("Clean House", "Deep clean and organize different areas of your home", "weekly"),
        ("Exercise Rest Day", "Take a complete rest from intense physical activity", "weekly"),
        ("Call Family", "Stay connected with family members through regular phone calls", "weekly"),
        ("Plan Next Week", "Review the upcoming week and set priorities and goals", "weekly"),
        
        # Monthly habits
        ("Budget Review", "Review your income, expenses, and financial goals", "monthly"),
        ("Update Resume", "Keep your resume current with new skills and experiences", "monthly"),
        ("Backup Data", "Create backups of important files and documents", "monthly"),
        ("Car Maintenance", "Check and maintain your vehicle (oil, tires, etc.)", "monthly"),
        ("Social Meetup", "Organize or attend social gatherings with friends", "monthly"),
        
        # Quarterly habits
        ("Skill Development", "Enroll in a course or workshop to learn something new", "quarterly"),
        ("Wardrobe Review", "Assess and update your clothing and accessories", "quarterly"),
        ("Investment Review", "Review and rebalance your investment portfolio", "quarterly"),
        
        # Annual habits
        ("Health Check-Up", "Schedule and attend comprehensive health examinations", "annually"),
        ("Goal Setting", "Set major life and career goals for the year", "annually"),
        ("Tax Preparation", "Organize documents and prepare annual tax returns", "annually"),
    ]
    
    base_time = datetime.now() - timedelta(days=60)  # Start habits 60 days ago
    habits = []
    
    for name, description, period in habits_data:
        # Add some randomness to creation times
        creation_time = base_time + timedelta(days=random.randint(0, 20))
        habit = Habit(
            name=name,
            task_description=description,
            period=period,
            creation_time=creation_time
        )
        habits.append(habit)
    
    return habits


def create_demo_users_with_habits(habits, days_of_data=30, min_completion_rate=0.6, max_completion_rate=0.9):
    """
    Create demo users with realistic habit tracking patterns.
    
    Args:
        habits: List of available habits
        days_of_data: Number of days of historical data to generate
        min_completion_rate: Minimum completion rate for habits
        max_completion_rate: Maximum completion rate for habits
    
    Returns:
        List[User]: List of demo users with tracked habits
    """
    user_profiles = [
        {
            "username": "fitness_enthusiast",
            "preferred_habits": [
                "Morning Exercise", "Drink Water", "Take Vitamins", 
                "Meditate", "Meal Planning", "Health Check-Up"
            ],
            "completion_bias": 0.85  # High completion rate
        },
        {
            "username": "busy_professional", 
            "preferred_habits": [
                "Review Daily Goals", "Budget Review", "Update Resume",
                "Skill Development", "Goal Setting", "Investment Review"
            ],
            "completion_bias": 0.70  # Medium-high completion rate
        },
        {
            "username": "student_life",
            "preferred_habits": [
                "Read for 30 Minutes", "Practice Gratitude", "Meditate",
                "Plan Next Week", "Skill Development", "Social Meetup"
            ],
            "completion_bias": 0.65  # Medium completion rate
        },
        {
            "username": "family_organizer",
            "preferred_habits": [
                "Meal Planning", "Grocery Shopping", "Clean House", 
                "Call Family", "Car Maintenance", "Backup Data"
            ],
            "completion_bias": 0.75  # Medium-high completion rate
        },
        {
            "username": "wellness_seeker",
            "preferred_habits": [
                "Meditate", "Practice Gratitude", "Drink Water",
                "Exercise Rest Day", "Health Check-Up", "Social Meetup"
            ],
            "completion_bias": 0.80  # High completion rate
        }
    ]
    
    users = []
    habit_dict = {habit.name: habit for habit in habits}
    
    for profile in user_profiles:
        user = User(username=profile["username"])
        
        # Add preferred habits to user
        user_habits = []
        for habit_name in profile["preferred_habits"]:
            if habit_name in habit_dict:
                habit = habit_dict[habit_name]
                
                # Create UserHabit with creation time slightly after habit creation
                creation_time = habit.creation_time + timedelta(days=random.randint(1, 5))
                user_habit = UserHabit(habit=habit, creation_time=creation_time)
                
                # Generate completion data
                generate_completion_data(
                    user_habit, 
                    days_of_data, 
                    profile["completion_bias"]
                )
                
                user_habits.append(user_habit)
        
        user.habits = user_habits
        users.append(user)
    
    return users


def generate_completion_data(user_habit, days_of_data, completion_bias):
    """
    Generate realistic completion data for a user habit.
    
    Args:
        user_habit: UserHabit object to generate data for
        days_of_data: Number of days to generate data for
        completion_bias: Base probability of completing the habit (0.0 to 1.0)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_of_data)
    
    # Get all periods since the user started tracking this habit
    tracking_start = max(user_habit.creation_time, start_date)
    all_periods = user_habit.habit.get_all_periods_since(tracking_start)
    
    for period_start, period_end in all_periods:
        # Skip future periods
        if period_start >= end_date:
            continue
            
        # Calculate completion probability with some randomness
        # Add some weekly patterns (lower completion on weekends for some habits)
        day_of_week_factor = 1.0
        if user_habit.habit.period == "daily":
            # Weekend effect for daily habits
            if period_start.weekday() >= 5:  # Saturday = 5, Sunday = 6
                day_of_week_factor = 0.8
        
        # Add some monthly patterns (lower completion at month start/end)
        monthly_factor = 1.0
        if period_start.day <= 5 or period_start.day >= 25:
            monthly_factor = 0.9
        
        # Combine all factors
        completion_probability = completion_bias * day_of_week_factor * monthly_factor
        
        # Add some random variation
        completion_probability += random.uniform(-0.1, 0.1)
        completion_probability = max(0.0, min(1.0, completion_probability))
        
        # Decide whether to complete this period
        if random.random() < completion_probability:
            # Generate a random completion time within the period
            period_duration = period_end - period_start
            random_offset = timedelta(
                seconds=random.randint(0, int(period_duration.total_seconds()))
            )
            completion_time = period_start + random_offset
            
            # Don't add completions in the future
            if completion_time < end_date:
                user_habit.completion_times.append(completion_time)


def save_demo_data(users, habits, storage_file):
    """
    Save the generated demo data to the storage file.
    
    Args:
        users: List of User objects
        habits: List of Habit objects  
        storage_file: Path to the storage file
    """
    # Remove existing file if it exists
    if os.path.exists(storage_file):
        os.remove(storage_file)
    
    # Create storage interface
    storage = JsonStorageInterface(storage_file)
    
    print(f"Saving demo data to {storage_file}...")
    
    # Insert all habits
    for habit in habits:
        success = storage.insert_habit(habit)
        if not success:
            print(f"Warning: Failed to insert habit '{habit.name}'")
    
    # Insert all users and their habits
    for user in users:
        # First insert all user habits
        for user_habit in user.habits:
            success = storage.insert_user_habit(user_habit)
            if not success:
                print(f"Warning: Failed to insert user habit for '{user.username}' - '{user_habit.habit.name}'")
        
        # Then insert the user
        success = storage.insert_user(user)
        if not success:
            print(f"Warning: Failed to insert user '{user.username}'")
    
    print(f"Demo data successfully saved to {storage_file}")


def print_demo_data_summary(users, habits, days_of_data):
    """
    Print a summary of the generated demo data.
    
    Args:
        users: List of User objects
        habits: List of Habit objects
        days_of_data: Number of days of data generated
    """
    print("\n" + "="*60)
    print("DEMO DATA SUMMARY")
    print("="*60)
    
    print(f"Generated data covering: {days_of_data} days")
    print(f"Total habits created: {len(habits)}")
    print(f"Total users created: {len(users)}")
    
    # Habit breakdown by period
    period_counts = {}
    for habit in habits:
        period_counts[habit.period] = period_counts.get(habit.period, 0) + 1
    
    print(f"\nHabits by periodicity:")
    for period, count in sorted(period_counts.items()):
        print(f"  {period.capitalize()}: {count}")
    
    print(f"\nUsers and their habits:")
    for user in users:
        print(f"\n  {user.username}:")
        print(f"    Tracking {len(user.habits)} habits")
        for user_habit in user.habits:
            completion_count = len(user_habit.completion_times)
            print(f"    - {user_habit.habit.name} ({user_habit.habit.period}): {completion_count} completions")
    
    # Calculate total completions
    total_completions = sum(
        len(user_habit.completion_times) 
        for user in users 
        for user_habit in user.habits
    )
    print(f"\nTotal habit completions recorded: {total_completions}")
    
    print(f"\nTo use this demo data:")
    print(f"1. Run: python main.py")
    print(f"2. Select option 1 (Login with existing account)")
    print(f"3. Choose from users: {', '.join(user.username for user in users)}")
    
    print("="*60)


def main():
    """
    Main function to generate demo data with configurable parameters.
    """
    # Configuration parameters
    days_of_data = 30
    min_completion_rate = 0.6
    max_completion_rate = 0.9
    storage_file = "demo_data.json"
    
    print("Creating demo data for Pascal's Habit Tracker...")
    print(f"Configuration:")
    print(f"  Days of data: {days_of_data}")
    print(f"  Completion rate range: {min_completion_rate:.1%} - {max_completion_rate:.1%}")
    print(f"  Storage file: {storage_file}")
    print()
    
    # Generate habits
    print("Creating realistic habits...")
    habits = create_realistic_habits()
    
    # Generate users with habit tracking data
    print("Creating demo users with tracking data...")
    users = create_demo_users_with_habits(
        habits, 
        days_of_data, 
        min_completion_rate, 
        max_completion_rate
    )
    
    # Save to storage
    save_demo_data(users, habits, storage_file)
    
    # Print summary
    print_demo_data_summary(users, habits, days_of_data)


if __name__ == "__main__":
    main()