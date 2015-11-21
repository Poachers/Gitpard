# coding: utf-8
from Gitpard.apps.repository.models import Repository
from django.db import models


class Report(models.Model):

    ON_AUTORS = 1
    ON_FILES = 2

    FAILED = -1
    PREPARED = 0
    READY = 1

    KIND = (
        (ON_AUTORS, u"Отчёт по авторам"),
        (ON_FILES, u"Отчёт по файлам")
    )

    STATE = (
        (FAILED, u"Ошибка при составлении отчёта"),
        (PREPARED, u"Отчёт подготавливается"),
        (READY, u"Отчёт готов")
    )

    repository = models.ForeignKey(Repository)

    branch = models.CharField(
        max_length=50,
        verbose_name=u'Имя ветки'
    )

    datetime = models.DateTimeField(
        verbose_name=u'Дата подготовки отчёта'
    )

    mask = models.TextField(
        verbose_name=u'Маска'
    )

    kind = models.IntegerField(
        choices=KIND,
        verbose_name=u'Тип отчёта'
    )

    state = models.IntegerField(
        choices=STATE,
        verbose_name=u"Состояние"
    )

    report = models.TextField(
        verbose_name=u'Отчёт',
        blank=True
    )

    path = models.CharField(
        max_length=140,
        unique=True,
        verbose_name=u'Путь до отчёта на сервере',
        blank=True
    )
