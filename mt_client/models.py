from django.db import models


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

    id_auk = models.BigIntegerField()
    id_mt = models.BigIntegerField()
    essence = models.CharField(max_length=50)
    dt = models.DateTimeField(auto_now=False, auto_now_add=False)
    comment = models.CharField(max_length=150)

    class Meta:
        managed = False
