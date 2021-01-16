from auk_client.models import Container
from django.contrib import admin
from django.utils.html import escape, mark_safe

from mt_client.models import replicationauk


@admin.register(replicationauk)
class ReplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_auk_link', 'id_mt', 'action', 'essence', 'dt',)
    list_filter = ('action', 'essence',)
    search_fields = ('id_mt', 'id_auk',)
    fields = ('id_auk',)
    # A handy constant for the name of the alternate database.
    using = 'mtdb'
    containers = None

    def id_auk_link(self, obj: replicationauk):
        if obj:
            if obj.essence == 'platform':
                return mark_safe(f'<a target="_blank" \
href="http://auk.kuzro.ru/{obj.essence}/{obj.id_auk}">\
                {escape(obj.id_auk)}</a>')
            elif obj.essence == 'container':
                if not self.containers:
                    self.containers = [x for x in Container.objects.all()]
                print(self.containers)
                container = [
                    x for x in self.containers if x.auk_id == obj.id_auk]
                if container:
                    container = container[0]
                if not container:
                    return obj.id_auk
                if container.auk_platform_id:
                    return mark_safe(f'<a target="_blank" \
href="http://auk.kuzro.ru/platform/\
    {container.auk_platform_id}/{container.auk_id}">{escape(obj.id_auk)}</a>')
                else:
                    return obj.id_auk
            else:
                return obj.id_auk
        else:
            return None

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request,
                                                using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request,
                                                using=self.using, **kwargs)
