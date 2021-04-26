from django.db import models


TASK_STATUS = (
    ("c", "created"), 
    ("p", "progress"), 
    ("s", "success"),
    ("f", "failed")
)

class TaskModel(models.Model):
    lastrunned = models.DateTimeField(
        "lastrunned", auto_now=False, auto_now_add=False)
    taskname = models.CharField("taskname", max_length=50)
    status = models.CharField(max_length=1, choices=TASK_STATUS, default='c')
    fail = models.TextField("fail", blank=True, null=True)
    def __str__(self) -> str:
        return f"{self.taskname} - {self.lastrunned}"

    class Meta:
        verbose_name = "запуск"
        verbose_name_plural = "запуски"
