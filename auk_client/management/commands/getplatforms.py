import time
from datetime import datetime, timedelta

import requests
from auk_client.models import Platform
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from initcmds.models import TaskModel
from requests.auth import AuthBase


class Command(BaseCommand):
    help = 'Получение площадок'

    def handle(self, *args, **options):
        start_time = time.time()
        start_date = timezone.now()
        try:
            last_task = TaskModel.objects \
                .filter(taskname="getplatforms") \
                .latest('lastrunned')
        except:
            last_task = TaskModel.objects.create(
                taskname="getplatforms",
                lastrunned=datetime.now() - timedelta(
                    days=int(settings.FIRST_RUN_DAYS)
                )
            )
        self.stdout.write(self.style.SUCCESS(f'Last task: {last_task}'))
        platforms = get_paged('http://apiauk.kuzro.ru/platforms/',
                              "next", "results", last_task.lastrunned)

        db_platforms = [Platform(auk_id=platform["id"],
                                 mt_id=platform["ext_id"],
                                 created=platform["datetime_create"],
                                 updated=platform["datetime_update"],
                                 raw_json=platform)
                        for platform in platforms]
        elapsed = time.time()
        self.stdout.write(self.style.SUCCESS(
            "--- %s seconds ---" % (elapsed - start_time)))
        Platform.objects.bulk_create(db_platforms)
        elapsed = time.time()
        self.stdout.write(self.style.SUCCESS(
            "--- %s seconds ---" % (elapsed - start_time)))

        TaskModel.objects.create(
            taskname="getplatforms",
            lastrunned=start_date
        )

        elapsed = time.time()
        self.stdout.write(self.style.SUCCESS(
            "--- Total %s seconds ---" % (elapsed - start_time)))


def get_paged(url, next_field, data_field, upd_date):
    start_time = time.time()
    print(upd_date)
    print(f"get {url}", end=", ")

    s = requests.Session()
    s.auth = LogPassAuth("http://apiauk.kuzro.ru/token/login/",
                         settings.AUK_LOGIN, settings.AUK_PASS)
    print(upd_date.strftime("%Y-%m-%d %H:%M"))

    response = s.get(url, params={
        "datetime_update_after": upd_date.strftime("%Y-%m-%d %H:%M")
    }).json()
    print(f"got count {response['count']} items")

    data = response[data_field]

    while response[next_field]:
        response = s.get(response[next_field]).json()
        data += response[data_field]
        print(f"got {len(response[data_field])} items")

    print(f"Total get {len(data)} items")
    elapsed = time.time()
    print("--- Total net: %s seconds ---" % (elapsed - start_time))
    return data


class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers['Authorization'] = f'Token {self.token}'
        return r


class LogPassAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, post_url, email, password):
        self.post_url = post_url
        self.email = email
        self.password = password
        self.token = None

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        if not self.token:
            response = requests.post(self.post_url, json={
                "email": self.email,
                "password": self.password
            }).json()
            print(self.email)
            print(self.password)
            print(response)
            if response["auth_token"]:
                self.token = response["auth_token"]
            else:
                raise requests.RequestException(response)

        r.headers['Authorization'] = f'Token {self.token}'
        return r
