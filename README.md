# About this project
This project provides a simple habit tracker which can be user via a CLI.

# Installation
## Installing python
This project requires python 3.10 or higher. You can download python from [here](https://www.python.org/downloads/). 
Please follow the instructions on the website to install python on your system.

## Running the habit tracker
To start the habit tracker, open a shell in the main directory of this project and run the following command:
```
python main.py
```
You should now see the user selection menu of the habit tracker:
```
--- Please select an option ---
1: Login with existing account
2: Create a new account
q: Exit program
```

# Using the habit tracker
## Creating a user
To create a new user, select option 2 in the user selection menu. You will be prompted to enter a username:
```
--- Please enter your username ---
testuser2
```
If the username already exists, you will be prompted to enter a different username. If the username does not exist, 
you will be forwarded to the main menu of the habit tracker:
```
--- Welcome, testuser2! ---
1: Habit tracking (track habit completion, add habits to tracking)
2: Habit creation (create new habits and edit existing ones)
3: Habit analysis (view habit streaks)
q: Exit program
```
To login with an existing user, select option 1 in the user selection menu.

## Creating a new habit
To create a new habit, select option 2 in the main menu. You will be forwarded to the habit creation menu:
```
--- Habit creation ---
1: Create new habit
2: Edit habit task description
3: Delete existing habit
q: Return to main menu
```
Select option 1 to create a new habit. You will be prompted to enter a name, task description and periodicity for 
the habit:
```
--- Create new habit ---
Enter habit name: testhabit
Enter habit task description: test test test
Enter habit tracking period (daily, weekly, monthly, quarterly, annually): monthly
testhabit created.
```

## Tracking a habit
In order to track a habit, you need to select option 1 in the main menu. You will be forwarded to the habit tracking menu:
```
--- Habit tracking ---
1: Track habit completion
2: Add habit to tracking
3: Remove habit from tracking
q: Return to main menu
```
First, you need to add a habit to the tracking list. Select option 2 and you will be prompted to select the habit you 
want to track:
```
--- Add habit to tracking ---
--- Please select a habit ---
1: take out trash
2: testhabit
q: Return to previous menu
Page 1 / 1
2
testhabit added to tracking.
```
Now you can mark the habit as completed. Select option 1 in the habit tracking menu and you will be prompted to select
the habit you want to mark as completed:
```
--- Track habit completion ---
--- Please select a habit ---
1: testhabit
q: Return to previous menu
Page 1 / 1
1
Press enter to mark testhabit as completed for today.
Alternatively, type a date in the format YYYY-MM-DD to mark a different date as completed.

testhabit marked as completed for today.
```
Please be aware that you can't mark the habit as completed for a point in time before you started tracking the habit. 
It is also not possible to mark a habit as completed multiple times in the same period, or for a date in the future.

## Habit analysis
You can use the habit analysis menu to view the streaks of your habits. Select option 3 in the main menu to access the
habit analysis menu:
```
--- Habit analysis ---
1: Show all habits with current streak
2: Show all habits with current streak for specific periodicity
3: Get habit with all-time longest streak
4: Get habit with current longest streak
5: Get longest streak for specific habit
6: Get longest all-time streak for specific habit
q: Return to main menu
```
You have different options to analyze your habits. For example, you can view all habits with their current streaks by
selecting option 1:
```
--- Habits with current streak ---
testhabit: 1
```
