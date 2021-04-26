import time
from datetime import timedelta

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from initcmds.models import TaskModel
from mt_client.models import replicationauk
from requests.auth import AuthBase


class Command(BaseCommand):
    help = 'Передача данных из МТ в AUK'

    def handle(self, *args, **options):
        start_time = time.time()
        start_date = timezone.now()
        try:
            last_task = TaskModel.objects \
                .filter(taskname="auk_post") \
                .latest('lastrunned')
        except:
            last_task = TaskModel.objects.create(
                taskname="auk_post",
                lastrunned=timezone.now() - timedelta(
                    days=int(settings.FIRST_RUN_DAYS)
                )
            )

        self.stdout.write(self.style.SUCCESS(f'Last task: {last_task}, {last_task.status}'))
        
        if last_task.status is "p":
            self.stdout.write(self.style.SUCCESS(
                "--- Task already in progress ---"))
            elapsed = time.time()
            self.stdout.write(self.style.SUCCESS(
                "--- Total %s seconds ---" % (elapsed - start_time)))
            return 

        if last_task.status in ["s", "f"]:
            last_task = TaskModel.objects.create(
                taskname="auk_post",
                lastrunned=start_date
            )

        platforms = [x for x in replicationauk.objects.using(
            "mtdb").all().filter(owner="mt", essence="platform")]
        containers = [x for x in replicationauk.objects.using(
            "mtdb").all().filter(owner="mt", essence="container")]

        elapsed = time.time()
        self.stdout.write(self.style.SUCCESS(
            "--- %s seconds ---" % (elapsed - start_time)))

        s = requests.Session()
        s.auth = LogPassAuth("http://apiauk.kuzro.ru/token/login/",
                             settings.AUK_LOGIN, settings.AUK_PASS)

        last_task.status = "p"
        last_task.save()

        try:
            for x in platforms:
                res = None
                if x.action == "insert":
                    res = s.post("http://apiauk.kuzro.ru/platforms/", json=x.attribute)
                elif x.action == "update":
                    res = s.patch(
                        f"http://apiauk.kuzro.ru/platforms/{x.id_auk}/",
                        json=x.attribute)
                elif x.action == "delete":
                    print("Not implemented")

                if res:
                    if res.status_code != 200:
                        print(f"{res.status_code} -- {res.content}")

                replicationauk.objects.using("mtdb").filter(id=x.id).delete()

            for x in containers:
                res = None
                if x.action == "create":
                    res = s.post("http://apiauk.kuzro.ru/containers/", json=x.attribute)
                elif x.action == "update":
                    res = s.patch(
                        f"http://apiauk.kuzro.ru/containers/{x.id_auk}/",
                        json=x.attribute)
                elif x.action == "delete":
                    print("Not implemented")

                if res:
                    if res.status_code != 200:
                        print(f"{res.status_code} -- {res.content}")

                replicationauk.objects.using("mtdb").filter(id=x.id).delete()
                replicationauk.objects.using("mtdb").filter(id=x.id).delete()

            elapsed = time.time()
            self.stdout.write(self.style.SUCCESS(
                "--- %s seconds ---" % (elapsed - start_time)))

            last_task.status = "s"
            last_task.save()
        except BaseException as e:
            last_task.status = "f"
            last_task.save()
            msg = str("\n".join(filter(None, map(str, list(e.args)))))
            last_task.fail = msg
            self.stdout.writse(self.style.ERROR(msg))
        finally:
            elapsed = time.time()
            self.stdout.write(self.style.SUCCESS(
                "--- Total %s seconds ---" % (elapsed - start_time)))


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

            if response["auth_token"]:
                self.token = response["auth_token"]
            else:
                raise requests.RequestException(response)

        r.headers['Authorization'] = f'Token {self.token}'
        return r
