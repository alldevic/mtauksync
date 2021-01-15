from django.db import models
from mt_client.fields import UnixTimestampField
ACTIONS = (
    ('insert', 'insert'),
    ('update', 'update'),
    ('delete', 'delete'),
)

OWNERS = (
    ('mt', 'mt'),
    ('auk', 'auk'),
)


class replicationauk(models.Model):
    #     CREATE TABLE replicationauk (
    #   id_auk bigint(20) DEFAULT NULL,
    #   id_mt bigint(20) DEFAULT NULL,
    #   action enum ('insert', 'update', 'delete') NOT NULL,
    #   essence varchar(50) DEFAULT NULL COMMENT 'сущность',
    #   dt datetime DEFAULT NULL COMMENT 'дата изменения в АУК',
    #   dtupdate timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    #   comment varchar(150) DEFAULT NULL
    # )

    id_auk = models.BigIntegerField(null=True)
    id_mt = models.BigIntegerField(null=True)
    action = models.CharField(max_length=20, choices=ACTIONS)
    essence = models.CharField(max_length=50)
    dt = models.DateTimeField(auto_now=False, auto_now_add=False)
    dtupdate = UnixTimestampField()
    comment = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'replicationauk'


class replicationauk21(models.Model):
    # CREATE TABLE 		 (
    #   id_auk bigint(20) DEFAULT NULL,
    #   id_mt bigint(20) DEFAULT NULL,
    #   owner varchar(15) DEFAULT NULL COMMENT 'система создавшая запись',
    #   action enum ('insert', 'update', 'delete') NOT NULL,
    #   essence varchar(50) NOT NULL COMMENT 'сущность',
    #   dt datetime DEFAULT NULL COMMENT 'дата изменения в АУК',
    #   dtupdate timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    #   comment varchar(150) DEFAULT NULL,
    #   attribute json DEFAULT NULL
    # )
    # ENGINE = INNODB,
    # AVG_ROW_LENGTH = 83,
    # CHARACTER SET utf8,
    # COLLATE utf8_general_ci;

    id_auk = models.BigIntegerField(null=True, default=None)
    id_mt = models.BigIntegerField(null=True, default=None)
    owner = models.CharField(
        max_length=20, choices=OWNERS, null=True, default=None)
    action = models.CharField(max_length=20, choices=ACTIONS)
    essence = models.CharField(max_length=50)
    dt = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    dtupdate = UnixTimestampField()
    comment = models.CharField(max_length=150)
    attribute = models.JSONField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'replicationauk_21'
