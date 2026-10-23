import json
import csv
from Task import Task

import api_client
import db


def get_tasks_as_string(tasks):
    text=""
    if not tasks:
        text = "Список задач пуст"
        return text
    for task in tasks:
        text += str(task)
    return text

def show_tasks(tasks):
    print(get_tasks_as_string(tasks))

def save_to_json(filename, tasks):
    tasks_dict_list=convert_Tasks_in_taskDictList(tasks)
    try:
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(tasks_dict_list, file, ensure_ascii=False, indent=4)
        print("Запись в файл успешно завершена ✅")
    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")

def load_from_json(filename):
    tasks_list=[]
    try:
        with open(filename, "r", encoding='utf-8') as file:
            tasks_dict_list = json.load(file)
            for task in tasks_dict_list:
                tasks_list.append(convert_dict_in_Task(task))
    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")
    return tasks_list

def convert_dict_in_Task(task_dict):
    return Task(task_dict["id"],task_dict["title"],task_dict["priority"],task_dict["done"])

def export_to_csv(filename, tasks):
    try:
        with open(filename, "w", encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Задача", "Приоритет", "Статус"])
            for task in tasks:
                writer.writerow([task.id, task.title, task.priority, task.done])
    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")

def convert_Tasks_in_taskDictList(tasks):
    tasks_dict_list=[]
    for task in tasks:
        tasks_dict_list.append(task.to_dict())
    return tasks_dict_list

if __name__ == "__main__":
    db.init_db()
    db.add_task_to_db("Купить хлеб", "Высокий")
    db.add_task_to_db("Сделать ДЗ", "Низкий")
    todo_list=db.get_all_tasks()
    show_tasks(todo_list)
    db.mark_task_done(1)
    todo_list=db.get_all_tasks()
    show_tasks(todo_list)
    export_to_csv("report.csv", todo_list)
    save_to_json("tasks.json", todo_list)

    unsynced = db.get_unsynced_tasks()
    
    for task in unsynced:
        if api_client.sync_task_to_server(task):
            db.mark_task_synced(task.id)
    print(f"\n💡 Совет дня: {api_client.get_motivation()}")
    
    todo_list.clear() # Очищаем память (имитация перезапуска)
    print("\n--- Перезапуск ---")
    todo_list = db.get_all_tasks()
    show_tasks(todo_list)

