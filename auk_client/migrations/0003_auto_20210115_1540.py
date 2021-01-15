# Generated by Django 3.1.4 on 2021-01-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auk_client', '0002_platform_raw_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='auk_platform_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='container',
            name='raw_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
