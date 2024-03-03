import sqlite3
from datetime import date
from habit import Habit
from task import Task
from task_history import TaskHistory
import db

#Recalling existing functions from the modules imported:
def create_habit():
    """Before creatig a Task, a Habit needs to be created, 
    as it groups similar tasks"""

    print('Create a new Habit')
    print('*******************')
    name = input('Enter habit name: ')
   
    habit = Habit(name)
    habit.save()

def add_task_to_habit():
    """From a list of Habits it is possible to add a Task by selecting the Habit first"""

    habit_items = {}
    habits = db.get_habits()

    for idx, habit in enumerate(habits):
        habit_id, name, start_date = habit
        habit_items[idx] = (habit_id, name)

    print()
    print('-------------------------------')
    print('Choose a Habit:-')

    for item in sorted(habit_items.items(), key=lambda x: x[0]):
        print(f"{item[0]} : {item[1][1]}")  
#  show habit names
    print()
    choice = int(input('Choice: '))

    habit_id = habit_items[choice][0]


    name = input('Enter Task name: ')
   

    freqs = {'1': 'daily', '2': 'weekly', '3': 'monthly', '4': 'yearly'}

    print()
    print('How Often: ')
    print()
    print('--------------')
    print('\t1. Daily')
    print('\t2. Weekly')
    print('\t3. Monthly')
    print('\t4. Yearly')

    choice = input('Choice: ')
    
    frequency = freqs.get(choice, 'daily')      #   default to daily

    #habit_id = db.find_habit_id(habit_name)

    task = Task(name, frequency, habit_id)
    print('TASK', task)
    task.save()

def view_habits():
        
        habits = db.get_habits()
        if not habits:
            print("No habits found.")
            return None

        print('-' * 52)
        print(f"{'HABITS':^55}")
        print('-' * 52)
        print(f"{'NAME':^40}{'CREATED':^12}")
        print(f"{'|':->40}{'|':->12}")

        for habit in habits:
            habit_id, name, created = habit
            print(f"{name:<40}{created}")
        print('-' * 52)

def view_tasks():
        tasks = db.get_tasks()
        if not tasks:
            print("No tasks found.")
            return None
        
        print('-' * 112)
        print(f"{'TASKS':^112}")
        print('-' * 112)
        print(f"{'NAME':^40}{'REPEAT':^10}{'STATUS':^10}{'STATUS DATE':^12}{'HABIT':<38}")
        print(f"{'|':->40}{'|':->10}{'|':->10}{'|':->12}{'|':->40}")

        for task in tasks:
            task_id, name, repeat, status, status_date, habit = task
            print(f"{name:<40}{repeat:<10}{status:<10}{status_date:<12}{habit:<38}")

        print('-' * 112)
    
def check_off_task():
    """Check off a task as completed"""
    task_items = {}
    tasks = db.get_tasks()

    for idx, row in enumerate(tasks):
        task_items[idx] = row

    print('-------------------------------')

    for item in sorted(task_items.items(), key=lambda x: x[0]):
        print(f"{item[0]} : {item[1][1]}")  #   show taks names

    print()
    choice = int(input('Choice: '))
    task = task_items[choice]
    task_id = task[0]

    checked_entry = TaskHistory(task_id, 'checked', )
    checked_entry.save()

def view_task_history():
    """It show the operations done on the tasks"""
    task_items = {}
    tasks = db.get_tasks()

    for idx, task in enumerate(tasks):
        task_id, name, repeat, status, status_date, habit = task
        task_items[idx] = (task_id, name)

    print('-------------------------------')

    for item in sorted(task_items.items(), key=lambda x: x[0]):
        print(f"{item[0]} : {item[1][1]}")  #   show taks names

    print()
    choice = int(input('Choice: '))
  
    history = db.get_task_history(task_items[choice][0])

    print('-' * 82)
    print(f"{'TASK HISTORY':^82}")
    print('-' * 82)
    print(f"{'NAME':^40}{'REPEAT':^10}{'STATUS CHANGE':^16}{'EVENT DATE':^16}")
    print(f"{'|':->40}{'|':->10}{'|':->16}{'|':->16}")

    for event in history:
            name, repeat, status_change, event_date = event
            print(f"{name:<40}{repeat:<10}{status_change:<16}{event_date:<16}")

    print('-' * 82)           

def edit_task():
        """it is possible to edit the name and periodicity of an existing task"""

        task_items = {}
        tasks = db.get_tasks()

        for idx, row in enumerate(tasks):
            task_items[idx] = row

        print('-------------------------------')

        for item in sorted(task_items.items(), key=lambda x: x[0]):
            print(f"{item[0]} : {item[1][1]}")  #   show taks names

        print()
        choice = int(input('Choice: '))
        task = task_items[choice]
        task_id = task[0]
    
        new_name = input('Enter new name for the task: ')

        print('\t1. Daily')
        print('\t2. Weekly')
        print('\t3. Monthly')
        print('\t4. Yearly')
        print()
        freq = input('How Frequent: ')
    
        freqs = {'1': 'daily', '2': 'weekly', '3': 'monthly', '4': 'yearly'}
        new_periodicity = freqs.get(freq, 'daily')   
        #default to daily if no input

        habit_id = task[5]

        task = Task(new_name, new_periodicity, habit_id)
        task.update(task_id)

        print("Task updated successfully.")

def select_task_by_name():
    """Pick a task from its name"""
    tasks = view_tasks()
    if not tasks:
        return None
    task_name = input('Enter the name of the task: ')
    for task in tasks:
        if task[1].lower() == task_name.lower():
            return task[0]
    print("Task not found.")
    return None

def show_broken_tasks():
    """Show tasks not completed within the given periodicity"""
    broken_tasks = db.get_broken_habits()
    if not broken_tasks:
        print("No Broken Tasks found.")
        return None
        
    print('-' * 78)
    print(f"{'TASKS':^78}")
    print('-' * 78)
    print(f"{'NAME':^40}{'REPEAT':^10}{'DATE':^16}{'DAYS DIFF':^12}")
    print(f"{'|':->40}{'|':->10}{'|':->16}{'|':->12}")

    for task in broken_tasks:
        task_id, periodicity, event_date, diff = task
        print(f"{task_id:<40}{periodicity:>10}{event_date:>16}{diff:>12}")

def main_menu():
    while True:
        print()
        print("Main Menu:")
        print("1. View Habits")
        print("2. View Tasks")      
        print("3. Create Habit")
        print("4. Add Task to Habit")
        print("5. Edit Task")
        print("6. Check Off Task")
        print("7. View Task History")
        print("8. Show Broken Habits")
        print("9. Exit")
        print()

        choice = input("Enter choice (1-9): ")
        if choice == '1':
            view_habits()
        
        elif choice == '2':
            view_tasks()

        elif choice == '3':
            create_habit()

        elif choice == '4':
            add_task_to_habit()

        elif choice == '5':
            edit_task()
    
        elif choice == '6':
            check_off_task()
        
        elif choice == '7':
            view_task_history()

        elif choice == '8':
            show_broken_tasks()           

        elif choice == '9':
            print("See you soon! keep up with your habits!")
            break

if __name__ == "__main__":
    main_menu()
