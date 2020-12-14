from django.db import models


class TaskModel(models.Model):
    lastrunned = models.DateTimeField(
        "lastrunned", auto_now=False, auto_now_add=False)
    taskname = models.CharField("taskname", max_length=50)

    def __str__(self) -> str:
        return f"{self.taskname} - {self.lastrunned}"

    class Meta:
        verbose_name = "запуск"
        verbose_name_plural = "запуски"
