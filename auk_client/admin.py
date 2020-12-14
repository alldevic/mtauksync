from django.contrib import admin
from auk_client.models import (Container, Platform)


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('auk_id', 'mt_id', 'created', 'updated',)
    search_fields = ('auk_id', 'mt_id',)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('auk_id', 'mt_id', 'created', 'updated',)
    search_fields = ('auk_id', 'mt_id',)
