# Generated by Django 3.1.4 on 2021-04-26 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initcmds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='status',
            field=models.CharField(choices=[('c', 'created'), ('p', 'progress'), ('s', 'success')], default='c', max_length=1),
        ),
    ]
