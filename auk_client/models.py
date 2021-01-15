from django.db import models


class Container(models.Model):
    auk_id = models.IntegerField(name="auk_id", null=True, blank=True)
    mt_id = models.CharField(
        name="mt_id", max_length=50, null=True, blank=True)
    created = models.DateTimeField(
        "Created", auto_now=False, auto_now_add=False, null=True, blank=True)
    updated = models.DateTimeField(
        "Updated", auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = "контейнер"
        verbose_name_plural = "контейнеры"

    def __str__(self):
        return f"{self.auk_id} - {self.updated}"


class Platform(models.Model):
    auk_id = models.IntegerField(name="auk_id", null=True, blank=True)
    mt_id = models.CharField(
        name="mt_id", max_length=50, null=True, blank=True)
    created = models.DateTimeField(
        "Created", auto_now=False, auto_now_add=False, null=True, blank=True)
    updated = models.DateTimeField(
        "Updated", auto_now=False, auto_now_add=False, null=True, blank=True)
    raw_json = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "платформа"
        verbose_name_plural = "платформы"

    def __str__(self):
        return f"{self.auk_id} - {self.updated}"
