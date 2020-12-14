from datetime import timezone
from django.core.management.base import BaseCommand
from initcmds.models import TaskModel
from auk_client.models import (Container, Platform)
from mt_client.models import ACTIONS, replicationauk
from datetime import timedelta
import time
from django.utils import timezone


class Command(BaseCommand):
    help = 'Отправка данных в базу MT'

    def handle(self, *args, **options):
        start_time = time.time()
        start_date = timezone.now()
        try:
            last_task = TaskModel.objects \
                .filter(taskname="postdelta") \
                .latest('lastrunned')
        except:
            last_task = TaskModel.objects.create(
                taskname="postdelta",
                lastrunned=timezone.now() - timedelta(days=30)
            )

        self.stdout.write(self.style.SUCCESS(
            f'Last task: {last_task}'))

        db_containers = Container.objects.filter(
            updated__gte=last_task.lastrunned)
        db_platforms = Platform.objects.filter(
            updated__gte=last_task.lastrunned)
        # Calculate delta
        mt_data = [replicationauk(id_auk=x.id,
                                  action='update',
                                  essence="container",
                                  dt=x.updated) for x in db_containers]
        mt_data += [replicationauk(id_auk=x.id,
                                   id_mt=x.mt_id,
                                   action='update' if x.mt_id else "insert",
                                   essence="platform",
                                   dt=x.updated) for x in db_platforms]
        # Post delta
        if mt_data:
            replicationauk.objects.using('mtdb').bulk_create(mt_data)
            TaskModel.objects.create(
                taskname="postdelta",
                lastrunned=start_date
            )
        else:
            self.stdout.write(self.style.SUCCESS("No data"))
        # Create new task info

        elapsed = time.time()
        self.stdout.write(self.style.SUCCESS(
            "--- Total %s seconds ---" % (elapsed - start_time)))
