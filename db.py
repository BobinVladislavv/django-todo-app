import sqlite3

from Task import Task

def init_db():
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (" \
        "id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "title TEXT NOT NULL," \
        "priority TEXT," \
        "done BOOLEAN DEFAULT 0," \
        "synced BOOLEAN DEFAULT 0" \
        ");")
        print("База данных инициализирована ✅")

def add_task_to_db(title, priority):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE title = ? AND priority = ?", (title, priority))
        if cursor.fetchone() is not None:
            print(f"Задача «{title}» уже существует, пропускаем.")
            return None
        cursor.execute("INSERT INTO tasks (title, priority, done, synced) VALUES (?, ?, 0, 0)", (title, priority))
        return cursor.lastrowid

def get_all_tasks():
    tasks_list = []
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        for row in rows:
            tasks_list.append(row_to_task(row))
    return tasks_list

def row_to_task(row):
    return Task(row[0],row[1],row[2],bool(row[3]),bool(row[4]))

def mark_task_done(task_id):
     with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        return cursor.rowcount > 0

def delete_task_from_db(task_id):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cursor.rowcount > 0

def find_task_by_id(task_id):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return row_to_task(row)

def get_unsynced_tasks():
    tasks_list=[]
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE synced = 0")
        rows = cursor.fetchall()
        for row in rows:
            tasks_list.append(row_to_task(row))
    return tasks_list

def mark_task_synced(task_id):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET synced = 1 WHERE id = ?", (task_id,))
        return cursor.rowcount > 0
    