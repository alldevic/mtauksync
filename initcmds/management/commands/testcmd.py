from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Отправка тестового сообщения'

    def handle(self, *args, **options):
        print("test")
