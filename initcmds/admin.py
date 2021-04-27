from django.contrib import admin

from initcmds.models import TaskModel


@admin.register(TaskModel)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('taskname', 'lastrunned','status')
    search_fields = ('taskname', 'status')
    list_filter = ('taskname', 'status')
