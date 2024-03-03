# importing the database createdwith sqlite3
# /Users/imanjouhar/WORKSPACES/habits_app/db.db
import sqlite3
database = '/Users/imanjouhar/WORKSPACES/habits_app/db5.db'

# database utility methods including select statements:

def find_habit_id(name : str) -> int:
            print('GET HABIT ID:'  + name + ':')
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  results = cursor.execute('SELECT  * from HABIT  where name = ? ',   (name,))

                  habit_id = results.fetchone()[0]

                  return habit_id
            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close()   


def find_task_id(name : str) -> int:
            print('GET TASK ID:'  + name + ':')
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  results = cursor.execute('SELECT  * from TASK  where name = ? ',   (name,))

                  task_id = results.fetchone()[0]

                  return task_id
            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close()  


def get_task_by_id(id : int) -> int:
            print('GET TASK BY ID:'  + str(id) + ':')
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  results = cursor.execute('SELECT  * from TASK  where task_id = ? ',   (id,))

                  rec = results.fetchone()

                  return rec
            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close()  

def get_habits():
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  results = cursor.execute('select habit_id, name, start_date from habit')
                  
                  habits = results.fetchall()
                  return habits
            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close()   

def get_tasks() :
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  results = cursor.execute('select t.task_id, t.name, t.periodicity, t.status, t.status_date, h.name from task t, habit h where t.habit_id = h.habit_id order by t.habit_id')
                  
                  tasks = results.fetchall()
                  return tasks
            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close() 



def update_task(name, periodicity, status, status_date, task_id):
            print('EDIT TASK for :', task_id )
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  cursor.execute("UPDATE TASK SET NAME = ?, PERIODICITY = ?, STATUS = ?, STATUS_DATE = ? WHERE TASK_ID = ?", (name, periodicity, status, status_date, task_id))
                  db.commit()                 

            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close()       


def get_task_history(task_id):
            """Queries the history of the task from the database."""
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  results = cursor.execute('select t.name, t.periodicity, h.status_change, h.event_date from task t, task_history h where t.task_id = h.task_id and t.task_id = ?', (task_id,))
                  
                  records = results.fetchall()
                  return records
            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close() 

def get_broken_habits():
            """Queries the history of the task from the database and compare with periodicity."""
            try:
                  db = sqlite3.connect(database)
                  cursor = db.cursor()

                  results = cursor.execute( """
                              select t.name, t.periodicity, b.event_date, b.diff 
                              from task t, broken_task b 
                              where t.task_id = b.task_id
                              and diff > CASE t.periodicity
                                    WHEN 'daily' THEN 1
                                    WHEN 'weekly' THEN 7
                                    WHEN 'monthly' THEN 30
                                    WHEN 'yearly' THEN 365
                                    END """)
                  
                  records = results.fetchall()
                  return records
            
            except sqlite3.Error as e:
                  print(f"An error occurred: {e}")
            finally:
                  db.close() 



