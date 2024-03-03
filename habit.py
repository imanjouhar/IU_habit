import sqlite3
from task import Task
from db import database
from datetime import date

class Habit:
    """A class to represent a habit within the application. 
    A habit can group one or more Tasks.

    Attributes:
        name (str): The name of the task.
        start_date (date): The date the app was created.
        periodicity (str): day, week, month, year to select for when the whole habit should be completed. 
    For example the user can select a habit for one month to lose weight, but within the habit there 
    could be several tasks to accomplish it: eat healthier, run every day, or swim will correspond to
    different tasks within the habit objective.
        """
    def __init__(self, name):
        self.name = name
        self.create_date = date.today()
        self.tasks = []

    def __str__(self):
        return 'Name: ' + self.name  + ' Tasks: ' + str(len(self.tasks))

    def add_task(self, task):
        """Each habit will have one or more tasks. 
        It is possible to add the task to a habit once created the habit first"""
        self.tasks.append(task)
        
    def get_warnings(self):
        """Provide warnings for tasks that are due within the week and haven't been checked off."""
        warnings = []
        today = date.today()
        for task in self.tasks:
            due_date = task.get_next_date()
            if due_date and 0 <= (due_date - today).days < 7:
                warnings.append(f"Warning: Task expiring '{task.name}' is due soon (Due Date: )")
        return warnings       

    def is_habit_broken(self):
        """A habit is broken when it has one or more broken tasks. 
        This method will show the broken habits."""
        for task in self.tasks:
            self.is_task_broken()


    def show(self):
        # Show the tasks in the habit:
        print(f' **** {self.name} ****')

        for task in self.tasks:
            habit_id, name, status, status_date = task[0], task[1].strip(), task[2], task[3]
            print(f'        :{name:<40}:{status:<10}:{status_date}')

    def get_tasks_count(self):
        """counting the tasks, methos useful for the Command line Interface"""
        return len(self.tasks)

    def save(self):
        """This metod saves the habit objects inserted
        by the user to the databse"""
        try:
            db = sqlite3.connect(database)
            cursor = db.cursor()
            cursor.execute('INSERT INTO HABIT(name) VALUES (?)', (self.name,))           
            pk = cursor.lastrowid
            #print('HABIT pk:', pk)
            db.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()
        return pk

    def load_tasks(self):
        """The task will be created from the habit, 
        the user will select the habit to create the task or will have
        the habit just created where he could add tasks. 
        This method is useful to the CLI"""
        print(self.name)
        try:
            db = sqlite3.connect(database)
            cursor = db.cursor()

            print('>>>>>>>>>>>>>')
            results = cursor.execute('SELECT  habit_id from HABIT where name = ? ',   (self.name,))
            print('>>>>>>>>>>>>>>>')
            habit_id = results.fetchone()[0]
            #for x in habit_id:
            print('XXXX', habit_id)

            print('-------')
            results = cursor.execute('SELECT  task_id, name, status, status_date  FROM TASK where habit_id = ?', (habit_id,))
            print('-------')
            self.tasks = results.fetchall()
            cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()

    @classmethod
    def find_habit(cls, name):
                    """it is important for the user to find habits
                    from the list of descriptions of habits.
                    this function will be used on the command line interface."""
                    print('TO CLASS: '  + name + ': ')
                    try:
                            db = sqlite3.connect(database)
                            cursor = db.cursor()

                            results = cursor.execute('SELECT  * from HABIT  where name = ? ',   (name,))
                            #for res in results.fetchall():
                             #    print(res)
                            habit_id = results.fetchone()[0]
                            #for x in habit_id:
                            print('Habit ID: ', habit_id)
                    except sqlite3.Error as e:
                        print(f"An error occurred: {e}")
                    finally:
                        db.close()

               