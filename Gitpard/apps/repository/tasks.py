# -*- coding: utf-8 -*-
import errno

import git
import django

django.setup()
import shutil

import os
import git
import stat
from rest_framework import viewsets, status as status_codes, exceptions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.utils import timezone
from Gitpard.apps.repository import serializers
from Gitpard.apps.repository.models import Repository
from Gitpard.apps.repository.helpers import get_url
from celery import task
from Gitpard.apps.repository.models import Repository


@task(ignore_result=True)
def update(obj_id):
    status = {}
    obj = Repository.objects.get(pk=obj_id)
    if not (obj.state == Repository.LOADED or obj.state == Repository.FAIL_UPDATE):
        status["code"] = -1
        status["message"] = u"Репозиторий не был склонирован"
        return status
    try:
        obj.state = Repository.UPDATE
        obj.save()
        status["code"] = 5
        status["message"] = u"Репозиторий обновляется"
        repo = git.Repo.init(obj.path)
        repo.git.fetch("origin")
        repo.git.reset("--merge")
        for ref in repo.remote("origin").refs:
            if ref.remote_head == "HEAD":
                continue
            repo.git.checkout(ref.remote_head)
            repo.git.pull("origin", ref.remote_head, v=True)
        obj.state = Repository.LOADED
        obj.save()
        status["code"] = 1
        status["message"] = u"Репозиторий обновлен"
    except git.GitCommandError as e:
        obj.state = Repository.FAIL_UPDATE
        if str(e).find("not found") != -1:
            status["code"] = -2
            status["message"] = u"Репозиторий не найден"
        elif str(e).find("Authentication failed") != -1:
            status["code"] = -3
            status["message"] = u"Ошибка авторизации"
        else:
            print "Update error: " + str(e)
            status["code"] = -4
            status["message"] = u'Ошибка сервера'
    except Exception as e:
        obj.state = Repository.FAIL_UPDATE
        print "Update error: " + str(e)
        status["code"] = -4
        status["message"] = u'Ошибка сервера'
    finally:
        obj.last_modify = timezone.now()
        obj.save()
        return status


@task(ignore_result=True)
def clone(obj_id):
    """Клонирование репозитория"""
    obj = Repository.objects.get(pk=obj_id)
    status = {}
    if not (obj.state == Repository.NEW or
            obj.state == Repository.FAIL_LOAD):
        status["code"] = -1
        status["message"] = u"Репозиторий уже был склонирован"
        return status
    try:
        obj.state = Repository.LOAD
        obj.save()
        status["code"] = 5
        status["message"] = u"Репозиторий клонируется"
        git.Repo.clone_from(get_url(obj), obj.path)
        repo = git.Repo.init(obj.path)
        repo.git.fetch("origin")
        repo.git.reset("--merge")
        for ref in repo.remote("origin").refs:
            if ref.remote_head == "HEAD":
                continue
            repo.git.checkout(ref.remote_head)
        obj.state = Repository.LOADED
        obj.save()
        status["code"] = 1
        status["message"] = u"Репозиторий склонирован"
    except git.GitCommandError as e:
        if os.path.exists(obj.path):
            shutil.rmtree(obj.path, ignore_errors=True)
        obj.state = Repository.FAIL_LOAD
        if str(e).find("not found") != -1:
            status["code"] = -2
            status["message"] = u"Репозиторий не найден"
        elif str(e).find("Authentication failed") != -1:
            status["code"] = -3
            status["message"] = u"Ошибка авторизации"
        else:
            print "Clone error: " + str(e)
            status["code"] = -4
            status["message"] = u"Ошибка сервера"
    except Exception as e:
        if os.path.exists(obj.path):
            shutil.rmtree(obj.path, ignore_errors=True)
        obj.state = Repository.FAIL_LOAD
        print "Clone error: " + str(e)
        status["code"] = -4
        status["message"] = u"Ошибка сервера"
    finally:
        obj.last_modify = timezone.now()
        obj.save()
        return status

@task(ignore_result=True)
def delete(obj_id):
    obj = Repository.objects.get(pk=obj_id)
    """Удаление репозитория"""
    status = {}
    if not (obj.state == Repository.NEW or
                    obj.state == Repository.LOADED or
                    obj.state == Repository.FAIL_LOAD or
                    obj.state == Repository.FAIL_UPDATE):
        status["code"] = -1
        status["message"] = u"Ведётся обработка репозитория, удаление невозможно"
        return status

    def handle_remove_readonly(func, path, exc):  # Удаляет файлы если было отказано в доступе
        exc_value = exc[1]
        if func in (os.rmdir, os.remove) and exc_value.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            func(path)
        else:
            raise
    obj = Repository.objects.get(pk=obj_id)
    if os.path.exists(obj.path):
        status["code"] = 5
        status["message"] = u"Репозиторий удаляется"
        shutil.rmtree(obj.path, ignore_errors=False, onerror=handle_remove_readonly)
    obj.delete()
    status["code"] = 1
    status["message"] = u"Репозиторий удален"
    return status