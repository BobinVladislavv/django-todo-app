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




todo_list = []


