from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Task
import api_client

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks/index.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        title= request.POST.get("title")
        priority = request.POST.get("priority", "Средний")
        if title:
            Task.objects.create(user=request.user, title=title, priority=priority)
        return redirect("task_list")
    return redirect("task_list")

@login_required
def complete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id = task_id, user=request.user)
        task.done = True
        task.save()
    return redirect("task_list")

@login_required
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
    return redirect("task_list")

@login_required
def sync_tasks(request):
    if request.method == "POST":
        unsynced = Task.objects.filter(user=request.user, synced=False)
        total = unsynced.count()
        if total ==0:
            messages.info(request, "Все задачи синхронизированны")
            return redirect("task_list")
        
        success_count = 0
        for task in unsynced:
            if api_client.sync_task_to_server(task):
                task.synced = True
                task.save()
                success_count+=1
        if success_count == total:
            messages.success(request, f"Синхронизированно {success_count} задач!")
        elif success_count > 0:
            messages.warning(request, f"Синхронизированно {success_count} из {total} задач")
        else:
            messages.error(request, "Не удалось синхронизировать задачи")
    return redirect("task_list")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f"Добро пожаловать {username}!")
                return redirect("task_list")
        messages.error(request, "Неверный логин или пароль")
    else:
        form = AuthenticationForm()
    return render(request, "tasks/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Вы вышли из системы!")
    return redirect("login")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, f"Аккаунт создан. Добро пожаловать, {user.username}!")
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "tasks/register.html", {"form": form})
