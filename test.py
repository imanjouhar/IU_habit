import pytest
from datetime import date, timedelta
from habit import Habit
from task import Task
import sqlite3
import db
# pytest = '/Users/imanjouhar/WORKSPACES/habits_app/test.py'
import os
print (os.getcwd())
import sys

# Test Task Class
def test_task_creation():
        # Test the creation of a Task object.
        task = Task("Take vitamins", "daily", 1, 'new', date.today())
        assert task.name == "Take vitamins"
        assert task.periodicity == "daily"
        assert task.habit_id == 1

def test_create_multiple_tasks():
        habit_test = Habit("Test Habit")
        count_before = habit_test.get_tasks_count()
        task1 = Task("Test Task 1", "daily", 19, 'new', date.today())
        task2 = Task("Test Task 2", "daily", 19, 'new', date.today())
        habit_test.add_task(task1)
        habit_test.add_task(task2)
        count_after = habit_test.get_tasks_count()

        assert count_after == count_before + 2

def test_task_check_off():
        # Test checking off a task as completed.
        task = Task("Clean your windows", "monthly", 1, 'new', date.today())
        task.check_off()
        assert task.status == "checked"

def test_task_get_next_date():
        # Test calculating the next due date of a task.
        task = Task("Read a book", "daily", 1, 'new', date.today())
        next_date = task.get_next_date()
        assert next_date == date.today() + timedelta(days=1)

def test_habit_count():
#this test will check if there are more than 5 sample habits for testing:
        conn = sqlite3.connect(db.database)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM HABIT")
        dates = cursor.fetchone()
        print('Lenght', dates)
        assert dates[0] > 5

def test_task_save():
        # Test saving a task to the database.
        task = Task("Write a journal", "daily", 1, 'new', date.today())
        pk = task.save()
        assert pk is not None

# Test Habit Class
def test_habit_creation():
        # Test the creation of a Habit object.
        habit = Habit("Exercise Regularly")
        assert habit.name == "Exercise Regularly"

def test_add_task_to_habit():
        # Test adding a Task to a Habit
        habit = Habit("Exercise Regularly")
        task = Task("Run 5km", "daily", 1, 'new', date.today())
        habit.add_task(task)
        assert len(habit.tasks) == 1
        assert habit.tasks[0].name == "Run 5km"

def test_habit_save():
        # Test saving a habit to the database.
        habit = Habit("Meditation")
        pk = habit.save()
        assert pk is not None 

def test_get_warnings():
    
    """Test the get_warnings method on habits when a task is about 
    expiring. Create a habit and tasks for testing purposes"""
    habit = Habit("Fitness Goal")

    # Create tasks with different due dates
    # Task due today
    task1 = Task("Morning Run", "daily", 1, 'new', date.today())
    # Task due in 3 days
    task2 = Task("Evening Yoga", "daily", 1, 'new', date.today() - timedelta(days=1))
    # Task due in 7 days
    task3 = Task("Weekly Hiking", "weekly", 1, 'new', date.today() - timedelta(days=7))
    # Task not due within a week
    task4 = Task("Monthly Marathon", "monthly", 1, 'new', date.today() - timedelta(days=30))
    # Add tasks to habit
    habit.add_task(task1)
    habit.add_task(task2)
    habit.add_task(task3)
    habit.add_task(task4)

    # Get warnings
    warnings = habit.get_warnings()

    # Check if warnings are correct
    assert len(warnings) == 4
    assert "Morning Run" in warnings[0]
    assert "Evening Yoga" in warnings[1]
    assert "Weekly Hiking" in warnings[2]

if __name__ == "__main__": 
    pytest.main()
