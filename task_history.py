import sqlite3
from datetime import date, timedelta
from db import database

class TaskHistory:
    """
    class to represent a task history record
    """
    def __init__(self, task_id, status = 'new', status_date= date.today()):
        """
        In this class, the periodicity will set the deadline to a specific task
        for example when daily, the day after,
        when weekly exaclty after 7 days.
        monthly is set up to be 30 days
        yearly is 365 days.
        """
        self.task_id = task_id
        self.status = status
        self.status_date = status_date
       
    def __str__(self):
        """it calls it when using the print function for task"""
        return 'Status: ' + self.status + ', Date: ' + self.status_date
    
    def __repr__(self):
        """print constructor code needed to re-create"""
        return f'TaskHistory({self.task_id}, {self.status}, {self.status_date}'



    def save(self):
        """saves data added to Task History record to persistant storage"""
        try:
            db = sqlite3.connect(database)
            cursor = db.cursor()
            sql = "INSERT INTO task_history(status_change, event_date, task_id) VALUES (?, ?, ?)"
            print(sql)
            cursor.execute(sql, (self.status, self.status_date, self.task_id))
            db.commit()
            pk = cursor.lastrowid
            return pk
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            db.close()
        
