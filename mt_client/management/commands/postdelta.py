import time

from auk_client.models import Container, Platform
from django.core.management.base import BaseCommand
from mt_client.models import replicationauk


class Command(BaseCommand):
    help = 'Отправка данных в базу MT'

    def handle(self, *args, **options):
        start_time = time.time()

        db_containers = Container.objects.all()
        db_platforms = Platform.objects.all()
        # Calculate delta
        mt_data = [replicationauk(id_auk=x.id,
                                  action='update',
                                  # owner='auk',
                                  # attribute=x.raw_json,
                                  essence="container",
                                  dt=x.updated) for x in db_containers]
        mt_data += [replicationauk(id_auk=x.id,
                                   id_mt=x.mt_id,
                                   action='update' if x.mt_id else "insert",
                                   # owner='auk',
                                   # attribute=x.raw_json,
                                   essence="platform",
                                   dt=x.updated) for x in db_platforms]
        # Post delta
        if mt_data:
            replicationauk.objects.using('mtdb').bulk_create(mt_data)
            [ct.delete() for ct in db_containers]
            [pl.delete() for pl in db_platforms]
        else:
            self.stdout.write(self.style.SUCCESS("No data"))
        # Create new task info

        elapsed = time.time()
        self.stdout.write(self.style.SUCCESS(
            "--- Total %s seconds ---" % (elapsed - start_time)))
