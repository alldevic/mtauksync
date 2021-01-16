from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_q.models import Schedule


class Command(BaseCommand):
    help = 'Инициализация тасок'

    def handle(self, *args, **options):
        # Create or update containers task
        try:
            task = Schedule.objects.get(name='auk_containers')
            task.next_run = timezone.now()+timedelta(minutes=1)
            if task.minutes != int(settings.AUK_CONTAINER_PERIOD):
                task.minutes = int(settings.AUK_CONTAINER_PERIOD)
            task.save()
        except ObjectDoesNotExist:
            self.stdout.write(self.style.SUCCESS('Create auk_containers'))
            Schedule.objects.create(
                name='auk_containers',
                func='django.core.management.call_command',
                args='"getcontainers"',
                schedule_type=Schedule.MINUTES,
                minutes=settings.AUK_CONTAINER_PERIOD,
                next_run=timezone.now()+timedelta(minutes=1)
            )

        # Create or update platform task
        try:
            task = Schedule.objects.get(name='auk_platforms')
            task.next_run = timezone.now()+timedelta(minutes=1)
            if task.minutes != int(settings.AUK_PLATFORM_PERIOD):
                task.minutes = int(settings.AUK_PLATFORM_PERIOD)
            task.save()
        except ObjectDoesNotExist:
            self.stdout.write(self.style.SUCCESS('Create auk_platforms'))
            Schedule.objects.create(
                name='auk_platforms',
                func='django.core.management.call_command',
                args='"getplatforms"',
                schedule_type=Schedule.MINUTES,
                minutes=settings.AUK_PLATFORM_PERIOD,
                next_run=timezone.now()+timedelta(minutes=1)
            )

        # Create or update mt task
        try:
            task = Schedule.objects.get(name='mt_post')
            if settings.ENABLE_MT_SYNC:
                task.next_run = timezone.now()+timedelta(minutes=1)
                if task.minutes != int(settings.MT_PERIOD):
                    task.minutes = int(settings.MT_PERIOD)
                task.save()
            else:
                task.delete()
        except ObjectDoesNotExist:
            self.stdout.write(self.style.SUCCESS('Create mt_post'))
            if settings.ENABLE_MT_SYNC:
                Schedule.objects.create(
                    name='mt_post',
                    func='django.core.management.call_command',
                    args='"postdelta"',
                    schedule_type=Schedule.MINUTES,
                    minutes=settings.MT_PERIOD,
                    next_run=timezone.now()+timedelta(minutes=1)
                )

        # Create or update auk sync task
        try:
            task = Schedule.objects.get(name='auk_post')
            if settings.ENABLE_AUK_SYNC:
                task.next_run = timezone.now()+timedelta(minutes=1)
                if task.minutes != int(settings.AUK_PERID):
                    task.minutes = int(settings.AUK_PERIOD)
                task.save()
            else:
                task.delete()
        except ObjectDoesNotExist:
            self.stdout.write(self.style.SUCCESS('Create auk_post'))
            if settings.ENABLE_AUK_SYNC:
                Schedule.objects.create(
                    name='auk_post',
                    func='django.core.management.call_command',
                    args='"aukpost"',
                    schedule_type=Schedule.MINUTES,
                    minutes=settings.MT_PERIOD,
                    next_run=timezone.now()+timedelta(minutes=1)
                )
