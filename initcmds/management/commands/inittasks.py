from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Инициализация тасок'

    def handle(self, *args, **options):
        # Create containers task
        try:
            Schedule.objects.get(name='auk_containers')
        except ObjectDoesNotExist:
            self.stdout.write(self.style.SUCCESS('Create auk_containers'))
            Schedule.objects.create(
                name='auk_containers',
                func='django.core.management.call_command',
                args='"getcontainers"',
                schedule_type=Schedule.MINUTES,
                minutes=5
            )

        # Create platform task
        try:
            Schedule.objects.get(name='auk_platforms')
        except ObjectDoesNotExist:
            self.stdout.write(self.style.SUCCESS('Create auk_platforms'))
            Schedule.objects.create(
                name='auk_platforms',
                func='django.core.management.call_command',
                args='"getplatforms"',
                schedule_type=Schedule.MINUTES,
                minutes=5
            )
        # Create mt task
        try:
            Schedule.objects.get(name='mt_post')
        except ObjectDoesNotExist:
            self.stdout.write(self.style.SUCCESS('Create mt_post'))
            Schedule.objects.create(
                name='mt_post',
                func='django.core.management.call_command',
                args='"postdelta"',
                schedule_type=Schedule.MINUTES,
                minutes=3
            )
        pass
