from db import database
import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect(database)

def fetch_data(query, parameters=None):
    """
    Fetch data from the database.
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters or ())
        return cursor.fetchall()

def display_data(query, parameters=None, formatter=lambda x: x):
    """
    Execute a query on the databse and display the results.
    """
    try:
        data = fetch_data(query, parameters)
        for row in data:
            print(formatter(row))
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def get_summary_current_habits():
    """Show a summary of current habits."""
    query = "SELECT HABIT_ID, NAME, START_DATE FROM HABIT ORDER BY START_DATE"
    data = fetch_data(query)
    return data
    
def get_summary_current_tasks():
    """Show a summary of current tasks."""
    query = """
    SELECT TASK_ID, NAME, STATUS, STATUS_DATE, PERIODICITY, HABIT_ID
    FROM TASK
    ORDER BY PERIODICITY
    """
    data = fetch_data(query)
    return data

def get_tasks_by_periodicity():
    """Show tasks grouped by periodicity."""
    query = """
    SELECT PERIODICITY, COUNT(*) 
    FROM TASK 
    GROUP BY PERIODICITY
    """
    data = fetch_data(query)
    return data

def show_streaks_per_task(task_id):
    """Similar query to above but showing the streaks for one task
    a unique task per time will be shown, giving a specific task id"""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT event_date FROM TASK_HISTORY WHERE task_id = ? ORDER BY event_date", (task_id,))
        dates = cursor.fetchall()

        if not dates:
            print(f"No history found for task {task_id}")
            return

        streak = 1
        max_streak = 1
        previous_date = datetime.strptime(dates[0][0], '%Y-%m-%d')

        for date in dates[1:]:
            current_date = datetime.strptime(date[0], '%Y-%m-%d')
            if (current_date - previous_date).days == 1:
                streak += 1
            else:
                streak = 1
            max_streak = max(max_streak, streak)
            previous_date = current_date

        print(f"Longest streak for task {task_id}: {max_streak} days")

def show_percentage_completed_per_task():
    """
    Tasks are considered completed 100% when checked off
    the percentage can help showing an average of completed
    and open tasks.
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task_id, COUNT(*) as total, SUM(CASE WHEN status = 'checked' THEN 1 ELSE 0 END) as completed FROM task GROUP BY task_id")
        rows = cursor.fetchall()

        for row in rows:
            task_id, total, completed = row
            percentage = (completed / total) * 100
            print(f"Task {task_id}: {percentage:.2f}% completed")

def show_average_completion_current_tasks():
    """Show the average completion percentage of all current tasks together."""
    query = """
    SELECT AVG(CASE WHEN STATUS = 'completed' THEN 1 ELSE 0 END) * 100 AS avg_completion
    FROM TASK
    """
    result = fetch_data(query)
    avg_completion = result[0][0] if result else 0
    print(f"Average Completion Percentage of Current Tasks: {avg_completion:.2f}%")

def show_broken_task():
    """
    Tasks are considered 'broken' from the moment they were completed late 
    or not conpleted at all at their expiry date defined by the periodicity.
    All habits with broken tasks are as well broken.
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT t.task_id, t.name FROM TASK t WHERE t.status = 'ongoing' AND NOT EXISTS (SELECT 1 FROM TASK_HISTORY th WHERE th.task_id = t.task_id)")
        broken_tasks = cursor.fetchall()

        if broken_tasks:
            print("Broken Tasks (Started but not ongoing):")
            for task in broken_tasks:
                print(f"Task ID: {task[0]}, Name: {task[1]}")
        else:
            print("No broken tasks found.")

def longest_run_streak_all_tasks():
    """
    Calculates and returns the longest streak of consecutive task completions
    across all tasks in the Task table on sqllite3.
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task_id FROM TASK")
        all_tasks = cursor.fetchall()

        max_streak = 0
        max_streak_task_id = None

        for task in all_tasks:
            task_id = task[0]
            streak = calculate_streak_for_task(task_id)
            if streak > max_streak:
                max_streak = streak
                max_streak_task_id = task_id

        print(f"Longest streak is {max_streak} days for task ID {max_streak_task_id}")

def calculate_streak_for_task(task_id):
    """It calculates the streak for a specific given task id"""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT event_date FROM TASK_HISTORY WHERE task_id = ? ORDER BY event_date", (task_id,))
        dates = cursor.fetchall()

    if not dates:
        return 0

    streak = 1
    max_streak = 1
    previous_date = datetime.strptime(dates[0][0], '%Y-%m-%d')

    for date in dates[1:]:
        current_date = datetime.strptime(date[0], '%Y-%m-%d')
        if (current_date - previous_date).days == 1:
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)
        previous_date = current_date

    return max_streak

def longest_run_streak_given_task(task_id):
    """
    Calculates and displays the longest streak of consecutive task completions
    for a specified task, based on the Task history table.
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        max_streak = calculate_streak_for_task(task_id)
    return max_streak

print('Get summary current habits')
print('====================================')
get_summary_current_habits()

print('Get summary current tasks')
print('====================================')
get_summary_current_tasks()

print('Longest run streak per task:')
print('====================================')
longest_run_streak_given_task(21)

print('Calculate streak for task:')
print('====================================')
calculate_streak_for_task(21)

print('Get task by periodicitiy:')
print('====================================')
get_tasks_by_periodicity()

print('Show broken task:')
print('====================================')
show_broken_task()

print('Show average completion current tasks:')
print('====================================')
show_average_completion_current_tasks()

print('Show percentage completed per task:')
print('====================================')
show_percentage_completed_per_task()

print('Show streaks per task:')
print('====================================')
show_streaks_per_task(21)

print('Longest run streak all tasks:')
print('====================================')
longest_run_streak_all_tasks()
