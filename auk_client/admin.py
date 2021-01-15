from django.contrib import admin
from django.utils.html import escape, mark_safe

from auk_client.models import Container, Platform


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'auk_id', 'mt_id', 'created', 'updated',)
    search_fields = ('auk_id', 'mt_id',)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'auk_id_link', 'mt_id', 'created', 'updated',)
    search_fields = ('auk_id', 'mt_id',)

    def auk_id_link(self, obj: Platform):
        if obj:
            return mark_safe(f'<a href="http://auk.kuzro.ru/platform/{obj.auk_id}">\
                {escape(obj.auk_id)}</a>')
        else:
            return None
