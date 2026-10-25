from django.shortcuts import render, redirect
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
    return redirect("Task_list")