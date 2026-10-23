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

def get_tasks_as_string(tasks):
    text=""
    if not tasks:
        text = "Список задач пуст"
        return text
    for task in tasks:
        if task["done"]: done = "✅ Выполнено"
        else: done = "❌ Не выполнено"
        text += ("[%s] %s (Приоритет: %s) - %s\n" % (task["id"], task["title"], task["priority"], done))
    return text

def show_tasks(tasks):
    print(get_tasks_as_string(tasks))

def save_to_file(filename, tasks):
    try:
        with open(filename, "w", encoding='utf-8') as file:
            for task in tasks:
                file.write(f"{task["id"]}|{task["title"]}|{task["priority"]}|{task["done"]}\n")
        print("Запись в файл успешно завершена ✅")
    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")

def load_from_file(filename):
    try:
        with open(filename,"r",encoding='utf-8') as file:
            for line in file:
                task_string = line.strip()
                todo_list.append(get_task_from_string(task_string))
    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")

def get_task_from_string(text):
    values=text.split('|')
    task = {"id": values[0], "title": values[1], "priority": values[2], "done": values[3]=="True"}
    return task

todo_list=[]
if __name__ == "__main__":
    add_task("Купить хлеб", "Высокий")
    add_task("Сделать ДЗ", "Низкий")
    show_tasks(todo_list)
    todo_list[1]["done"]=True
    save_to_file("tasks.txt", todo_list)
    
    todo_list.clear() # Очищаем память (имитация перезапуска)
    print("\n--- Перезапуск ---")
    load_from_file("tasks.txt")
    show_tasks(todo_list)

