import json
import csv

class Task:
    def __init__(self, id, title, priority, done):
        self.id = id
        self.title = title
        self.priority = priority
        self.done = done

    def to_dict(self):
        return {"id": self.id, "title": self.title, "priority": self.priority, "done": self.done}

    def __str__(self):
        if self.done: done = "✅ Выполнено"
        else: done = "❌ Не выполнено"
        text="[%s] %s (Приоритет: %s) - %s\n" % (self.id, self.title, self.priority, done)
        return text

def create_task(title, priority):
    if not todo_list:
        task = Task(1,title,priority,False)
    else:
        task = Task(find_max_id(todo_list)+1,title,priority,False)
    return task

def find_max_id(tasks):
    max=0
    for task in tasks:
        if(task.id>max):
            max=task.id
    return max

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

todo_list=[]
if __name__ == "__main__":
    todo_list.append(create_task("Купить хлеб", "Высокий"))
    todo_list.append(create_task("Сделать ДЗ", "Низкий"))
    todo_list[1].done = True
    show_tasks(todo_list)
    export_to_csv("report.csv", todo_list)
    save_to_json("tasks.json", todo_list)
    
    todo_list.clear() # Очищаем память (имитация перезапуска)
    print("\n--- Перезапуск ---")
    todo_list = load_from_json("tasks.json")
    show_tasks(todo_list)

