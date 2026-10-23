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

def show_tasks(tasks):
    if tasks == None:
        print("Список задач пуст")
        return
    for task in tasks:
        if task["done"]: done = "✅ Выполнено"
        else: done = "❌ Не выполнено"
        print("[%s] %s (Приоритет: %s) - %s" % (task["id"], task["title"], task["priority"], done))

todo_list = []
add_task("1",1)
add_task("2",1)
add_task("2",1)
add_task("2",1)
show_tasks(todo_list)


