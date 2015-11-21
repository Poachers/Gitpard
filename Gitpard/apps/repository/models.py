# -*- coding: utf-8 -*-


from django.contrib.auth.models import User
from django.db import models

from Gitpard import settings


class Repository(models.Model):
    """Mодель репозитория."""

    # Вид репозитория
    PUBLIC = 0
    PRIVATE = 1

    # состояние
    NEW = 0
    LOAD = 1
    LOADED = 2
    UPDATE = 3
    FAIL_LOAD = -1
    FAIL_UPDATE = -2

    STATE = (
        (NEW, u'Не загружен'),
        (LOAD, u'Загружается'),
        (LOADED, u'Загружен'),
        (UPDATE, u'Обновляется'),
        (FAIL_LOAD, u'Не удалось загрузить'),
        (FAIL_UPDATE, u'Не удалось обновить'),
    )

    KIND = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private')
    )

    url = models.CharField(
        max_length=140, verbose_name=u'ссылка на репозиторий')
    path = models.CharField(
        max_length=140, unique=True,
        verbose_name=u'Путь до папки репозитория на сервере.')

    login = models.CharField(
        max_length=140, blank=True,
        verbose_name=u'Логин пользоватея для приватных репозиториев')
    password = models.CharField(
        max_length=50, blank=True,
        verbose_name=u'Пароль пользователя для приватных репозиториев')
    user = models.ForeignKey(User)
    name = models.CharField(
        max_length=140, blank=True, verbose_name=u'имя проекта')

    kind = models.IntegerField(choices=KIND, verbose_name=u'Тип репозитория.')
    state = models.IntegerField(
        choices=STATE, default=NEW, verbose_name=u'Состояние репозитория.')

    last_modify = models.DateTimeField(verbose_name=u'Дата последнего изменения')
    mask = models.TextField(verbose_name=u'Маска', blank=True)

    class Meta:
        unique_together = ("url", "user")

    def __unicode__(self):
        return self.name
