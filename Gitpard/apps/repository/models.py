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
    BLOCKED = 4  # Блокировка репозитория при его обработке
    FAIL_LOAD = -1
    FAIL_UPDATE = -2

    STATE = (
        (NEW, u'Не загружен'),
        (LOAD, u'Загружается'),
        (LOADED, u'Загружен'),
        (UPDATE, u'Обновляется'),
        (FAIL_LOAD, u'Не удалось загрузить'),
        (FAIL_UPDATE, u'Не удалось обновить'),
        (BLOCKED, u'Доступ заблокирован'),
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
        verbose_name_plural = "Repositories"
        unique_together = ("url", "user")

    def __unicode__(self):
        return self.name


# TODO вынести в базовое приложение
class RepoIssueLog(models.Model):
    """модель для логирования"""

    error = -1
    notification_issue = 0
    notification_success = 1

    TYPE = (
        (error, u'Ошибка'),
        (notification_success, u'Уведомление: задача выполнена'),
        (notification_issue, u'Уведомление: задача не выполнена'),
    )

    all = 0
    repository = 1
    analysis = 2
    report = 3

    MODULES = (
        (all, u'Все модули'),
        (repository, u'Модуль репозитории'),
        (analysis, u'Модуль анализ'),
        (report, u'Модуль отчёты'),
    )

    user = models.ForeignKey(User, null=True, blank=True)
    repo = models.ForeignKey(Repository)
    type = models.IntegerField(choices=TYPE, verbose_name=u'Тип')
    module = models.IntegerField(choices=MODULES, verbose_name=u'Модуль')
    message = models.CharField(max_length=140, verbose_name=u'Описание ошибки')
    description = models.TextField(verbose_name=u'Текст ошибки')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "RepoIssueLogs"

    def __unicode__(self):
        return self.message

    def to_json(self):
        return {
                "ts": self.created_at,
                "code": self.type,
                "repo_id": self.repo_id,
                "message": self.message,
                "description": self.description
            }