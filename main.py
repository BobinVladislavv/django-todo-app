def add_task(title, priority):
    if todo_list == None:
        task = {"id": 1, "title": title, "priority": priority, "done": False}
    else:
        task = {"id": find_max_id(todo_list)+1, "title": title, "priority": priority, "done": False}
    todo_list.append(task)

def find_max_id(tasks):
    max=0
    for task in tasks:
        if(task["id"]>max):
            max=task["id"]
    return max

def get_tasks(tasks):
    text=""
    if not tasks:
        text = "Список задач пуст"
        return text
    for task in tasks:
        if task["done"]: done = "✅ Выполнено"
        else: done = "❌ Не выполнено"
        text += ("[%s] %s (Приоритет: %s) - %s\n" % (task["id"], task["title"], task["priority"], done))
    return text

def save_to_file(filename, tasks):
    try:
        with open(filename, "w", encoding='utf-8') as file:
            file.write(get_tasks(tasks))
        print("Запись в файл успешно завершена ✅")
    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")

todo_list = []
filename = "tasks_list.txt"
add_task("Покушать", 1)
todo_list[0]["done"]=True
add_task("Попить", 2)
add_task("Поспать", 3)

print(get_tasks(todo_list))
save_to_file(filename, todo_list)


