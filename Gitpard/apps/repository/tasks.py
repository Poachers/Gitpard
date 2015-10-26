# coding: utf-8

import git
from celery import task
from Gitpard.apps.repository.models import Repository
from Gitpard.apps.repository.helpers import _get_url


@task(ignore_result=True)
def update(obj_id):
    obj = Repository.objects.get(pk=obj_id)
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
    print 'Repo ' + str(obj.id) +' update'

@task(ignore_result=True)
def clone(obj_id):
    obj = Repository.objects.get(pk=obj_id)
    git.Repo.clone_from(_get_url(obj), obj.path)
    obj.state = Repository.LOADED
    obj.save()
    print 'Repo ' + str(obj.id) +' clone'

@task(ignore_result=True)
def delete(obj_id):
    obj = Repository.objects.get(pk=obj_id)
    obj.delete()
    print 'Repo ' + str(obj.id) +' delete'