from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
import api_client

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
    if request.method == "POST":
        task = get_object_or_404(Task, id = task_id)
        task.done = True
        task.save()
    return redirect("task_list")

def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect("task_list")

def sync_tasks(request):
    if request.method == "POST":
        unsunced = Task.objects.filter(synced=False)
        total = unsunced.count()
        if total ==0:
            messages.info(request, "Все задачи синхронизированны")
            return redirect("task_list")
        
        succes_count = 0
        for task in unsunced:
            if api_client.sync_task_to_server(task):
                task.synced = True
                task.save()
                succes_count+=1
        if succes_count == total:
            messages.success(request, f"Синхронизированно {succes_count} задач!")
        elif succes_count > 0:
            messages.warning(request, f"Синхронизированно {succes_count} из {total} задач")
        else:
            messages.error(request, "Не удалось синхронизировать задачи")
    return redirect("task_list")