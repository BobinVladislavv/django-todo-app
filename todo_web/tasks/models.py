from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Высокий", "Высокий"),
        ("Средний", "Средний"),
        ("Низкий", "Низкий"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    priority = models.CharField(max_length=20,
                                choices=PRIORITY_CHOICES,
                                default="Средний",
                                verbose_name="Приоритет")
    done = models.BooleanField(default=False, verbose_name="Выполнено")
    synced = models.BooleanField(default=False, verbose_name="Синхронизированно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Задача"
        verbose_name_plural = "Задача"
        ordering = ["-created_at"]