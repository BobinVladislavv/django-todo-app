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