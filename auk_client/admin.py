import json
import logging

from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from django.utils.html import escape, mark_safe

from auk_client.models import Container, Platform

logger = logging.getLogger(__name__)


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'auk_id_link', 'mt_id', 'created', 'updated',)
    search_fields = ('auk_id', 'mt_id',)
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def auk_id_link(self, obj: Container):
        if obj:
            if obj.auk_platform_id:
                return mark_safe(f'<a target="_blank" \
href="http://auk.kuzro.ru/platform/{obj.auk_platform_id}/{obj.auk_id}">\
{escape(obj.auk_id)}</a>')
            else:
                return obj.auk_id
        else:
            return None


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'auk_id_link', 'mt_id', 'created', 'updated',)
    search_fields = ('auk_id', 'mt_id',)
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def auk_id_link(self, obj: Platform):
        if obj:
            return mark_safe(f'<a href="http://auk.kuzro.ru/platform/{obj.auk_id}">\
                {escape(obj.auk_id)}</a>')
        else:
            return None
