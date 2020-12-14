from django.contrib import admin

from initcmds.models import TaskModel


@admin.register(TaskModel)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('taskname', 'lastrunned',)
    search_fields = ('taskname',)
