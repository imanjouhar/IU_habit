import sqlite3
from datetime import date, timedelta
from db import database

class Task:
    """A class to represent a task within a habit tracking application.
        """
    def __init__(self, name, periodicity, habit_id, status = 'new', status_date= date.today()):
        """The periodicity listed above will set the deadline to a specific task
        for example when dayly, the day after,
        when weekly exaclty after 7 days.
        monthly is set up to be 30 days
        yearly is 365 days.
        """
        self.name = name
        self.periodicity = periodicity
        self.habit_id = habit_id
        self.status = status
        self.status_date = status_date
       
    def __str__(self):
        """It calls it when using the print function for task"""
        return 'Name: ' + self.name + ', Status: ' + self.status
    
    def __repr__(self):
        """Print from a list"""
        return 'Name: ' + self.name + ', Status: ' + self.status

    def get_task_history(self):
        """Queries the history of the task from the database."""
        history = []
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            cursor.execute("SELECT EVENT_DATE, STATUS_CHANGE FROM TASK_HISTORY WHERE TASK_ID = ?", (self.id,))
            history = cursor.fetchall()
        return history

    def get_next_date(self):
        """Calculate the next due date to complete the task."""
        if self.periodicity == 'daily':
            return self.status_date + timedelta(days=1)
        elif self.periodicity == 'weekly':
            return self.status_date + timedelta(days=7)
        elif self.periodicity == 'monthly':
            return self.status_date + timedelta(days=30)
        elif self.periodicity == 'yearly':
            return self.status_date + timedelta(days=365)
        else:
            return None

    def get_deadline(self):
        """
        It returns the deadline that the user sets on a specific task to be completed.
        """
        return self.deadline

    def check_off(self):
        """
        Marks the task as completed and updates the status date
        which was defaulted as ongoing. The user has the chance to change
        the status by checking it off.
        """
        self.status =  'checked'
        self.status_date = date.today()

    def _parse_date(date_str):
        """Parse date strings into date objects."""
        dd, mm, yy = map(int, date_str.split('/'))
        return date(yy, mm, dd)
    
    def save(self):
        """saves data added to Task to persistant storage
            on the respective table of the database, previously set up on sqlite3"""
        try:
            db = sqlite3.connect(database)
            cursor = db.cursor()
            sql = "INSERT INTO task(name, periodicity, status, status_date, habit_id) VALUES (?, ?, ?, ?, ?)"
            print(sql)
            cursor.execute(sql, (self.name, self.periodicity, self.status, self.status_date, self.habit_id))
            pk = cursor.lastrowid
            db.commit()
            return pk
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()

    def update(self, task_id):
            """method to update task from command line interface with sys"""
            print('UPDATE TASK for :' )
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  cursor.execute("UPDATE TASK SET NAME = ?, PERIODICITY = ?, STATUS = ?, STATUS_DATE = ? WHERE TASK_ID = ?", 
                                 (self.name, self.periodicity, self.status, self.status_date, task_id))
                  db.commit()                 

            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close()       
