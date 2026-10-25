from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/index.html", {"tasks": tasks})

def add_task(request):
    if request.method == "POST":
        title= request.POST.get("title")
        priority = request.POST.get("priority", "Средний")
        if title:
            Task.objects.create(title=title, priority=priority)
        return redirect("task_list")
    return redirect("task_list")

def complete_task(request, task_id):
    task = get_object_or_404(Task, id = task_id)
    task.done = True
    task.save()
    return redirect("task_list")

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("task_list")