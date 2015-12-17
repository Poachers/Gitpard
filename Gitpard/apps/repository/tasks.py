# -*- coding: utf-8 -*-
import shutil
import os
import git
import stat
from Gitpard import settings
from django.utils import timezone
from Gitpard.apps.repository.helpers import get_url
from celery.task import task
from Gitpard.apps.repository.models import Repository
import errno
import django
django.setup()


@task(ignore_result=True)
def update(obj_id):
    obj = Repository.objects.get(pk=obj_id)
    try:
        repo = git.Repo.init(obj.path)
        repo.git.fetch("origin")
        repo.git.reset("--merge")
        for ref in repo.remote("origin").refs:
            if ref.remote_head == "HEAD":
                continue
            repo.git.checkout(ref.remote_head)
            repo.git.pull("origin", ref.remote_head, v=True)
    except git.GitCommandError as e:
        obj.state = Repository.FAIL_UPDATE
        obj.save(update_fields=['state'])
        if settings.DEBUG:
            print "Update error: ", str(e)
    except Exception as e:
        obj.state = Repository.FAIL_UPDATE
        obj.save(update_fields=['state'])
        if settings.DEBUG:
            print "Update error: ", str(e)
    else:
        obj.state = Repository.LOADED
        obj.save(update_fields=['state'])
    finally:
        obj.last_modify = timezone.now()
        obj.save(update_fields=['last_modify'])


@task(ignore_result=True)
def clone(obj_id):
    obj = Repository.objects.get(pk=obj_id)
    try:
        git.Repo.clone_from(get_url(obj), obj.path)
        repo = git.Repo.init(obj.path)
        repo.git.fetch("origin")
        repo.git.reset("--merge")
        for ref in repo.remote("origin").refs:
            if ref.remote_head == "HEAD":
                continue
            repo.git.checkout(ref.remote_head)
    except git.GitCommandError as e:
        if os.path.exists(obj.path):
            shutil.rmtree(obj.path, ignore_errors=True)
        obj.state = Repository.FAIL_LOAD
        obj.save(update_fields=['state'])
        if settings.DEBUG:
            print "Clone error: ", str(e)
    except Exception as e:
        if os.path.exists(obj.path):
            shutil.rmtree(obj.path, ignore_errors=True)
        obj.state = Repository.FAIL_LOAD
        obj.save(update_fields=['state'])
        if settings.DEBUG:
            print "Clone error: ", str(e)
    else:
        obj.state = Repository.LOADED
        obj.save(update_fields=['state'])
    finally:
        obj.last_modify = timezone.now()
        obj.save(update_fields=['last_modify'])


@task(ignore_result=True)
def delete(obj_id):

    def handle_remove_readonly(func, path, exc):  # Удаляет файлы если было отказано в доступе
        exc_value = exc[1]
        if func in (os.rmdir, os.remove) and exc_value.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            func(path)
        else:
            raise

    obj = Repository.objects.get(pk=obj_id)
    if os.path.exists(obj.path):
        shutil.rmtree(obj.path, ignore_errors=False, onerror=handle_remove_readonly)
    obj.delete()
