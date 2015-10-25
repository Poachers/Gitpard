# coding: utf-8

import git
from celery import task
from Gitpard.apps.repository.models import Repository


@task(ignore_result=True)
def update(obj):
    repo = git.Repo.init(obj.path)
    repo.git.fetch("origin")
    for ref in repo.remote("origin").refs[1:]:
        repo.git.reset("--merge")
        repo.git.checkout(ref.remote_head)
        repo.git.pull("origin", ref.remote_head, v=True)
    #origin = repo.remote('origin') #Попробовать на сервере, может быть ошибки с удалением не будет
    #origin.fetch()
    #origin.pull()

    obj.state = Repository.LOADED
    obj.save()
    print 'vse))'

@task(ignore_result=True)
def clone(self, obj):
    git.Repo.clone_from(self._get_url(obj), obj.path)
    obj.state = Repository.LOADED
    obj.save()
    print 'vse clonnig epta :))'