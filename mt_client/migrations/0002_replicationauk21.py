# Generated by Django 3.1.4 on 2021-01-15 14:00

from django.db import migrations, models
import mt_client.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mt_client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='replicationauk21',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_auk', models.BigIntegerField(default=None, null=True)),
                ('id_mt', models.BigIntegerField(default=None, null=True)),
                ('owner', models.CharField(choices=[('mt', 'mt'), ('auk', 'auk')], default=None, max_length=20, null=True)),
                ('action', models.CharField(choices=[('insert', 'insert'), ('update', 'update'), ('delete', 'delete')], max_length=20)),
                ('essence', models.CharField(max_length=50)),
                ('dt', models.DateTimeField(null=True)),
                ('dtupdate', mt_client.fields.UnixTimestampField(null=True)),
                ('comment', models.CharField(max_length=150)),
                ('attribute', models.JSONField(null=True)),
            ],
            options={
                'db_table': 'replicationauk_21',
                'managed': False,
            },
        ),
    ]
