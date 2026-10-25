from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "priority", "done", "synced", "user", "created_at")
    list_filter = ("done", "priority", "synced", "user")
    search_fields = ("title",)
    list_editable = ("done",)

