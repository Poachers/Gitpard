# coding: utf-8

import os

import git
from Gitpard import settings
from rest_framework import viewsets, status as status_codes, exceptions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.contrib.auth.models import User
from Gitpard.apps.repository import serializers
from Gitpard.apps.repository.models import Repository
from Gitpard.apps.repository.helpers import get_url
from Gitpard.apps.repository.tasks import clone, update, delete


class RepositoryViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.RepositorySerializer
    queryset = Repository.objects
    async_methods = 3

    def check_repos_in_celery(self):
        user_repositeries = Repository.objects.filter(user=self.request.user)
        repo_in_celery = 0
        for repo in user_repositeries:
            if repo.state == 3 or repo.state == 1:
                repo_in_celery += 1
        return repo_in_celery

    @detail_route(methods=['get'])
    def clone(self, request, pk):
        status = {}
        allowed_states = [
            Repository.NEW,
            Repository.FAIL_LOAD
        ]
        obj = self.get_object()
        if not any([obj.state == allowed for allowed in allowed_states]):
            status["code"] = -1
            status["message"] = u"Репозиторий уже был склонирован"
        else:
            try:
                clone.delay(obj.id)
            except Exception as e:
                status["code"] = -2
                status["message"] = u"Ошибка при добавлении задачи"
                if settings.DEBUG:
                    print "Error while adding clone task: ", str(e)
            else:
                status["code"] = 1
                status["message"] = u"Задача добавлена"
        return Response({'status': status}, status=status_codes.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='update')
    def update_repo(self, request, pk):
        status = {}
        obj = self.get_object()
        allowed_states = [
            Repository.LOADED,
            Repository.FAIL_UPDATE,
        ]
        if not any([obj.state == allowed for allowed in allowed_states]):
            status["code"] = -1
            status["message"] = u"Невозможно обновить репозиторий"
        else:
            try:
                update.delay(obj.id)
            except Exception as e:
                status["code"] = -2
                status["message"] = u"Ошибка при добавлении задачи"
                if settings.DEBUG:
                    print "Error while adding update task: ", str(e)
            else:
                status["code"] = 1
                status["message"] = u"Задача добавлена"
        return Response({'status': status}, status=status_codes.HTTP_200_OK)

    @detail_route(methods=['get', 'post'])
    def edit(self, request, pk):
        obj = self.get_object()
        if not (obj.state == Repository.NEW or obj.state == Repository.FAIL_LOAD):
            self.serializer_class = serializers.RepositoryEditSerializer
        if request.method == 'GET':
            serializer = self.serializer_class(obj)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = request.data
            context = {
                "request": self.request,
                "pk": pk
            }
            serializer = self.serializer_class(obj, data=data, context=context)
            if serializer.is_valid():
                serializer.save()
                if os.path.exists(obj.path):
                    try:
                        repo = git.Repo.init(obj.path)
                        if repo.remote('origin') in repo.remotes:
                            repo.git.remote("set-url", "origin", get_url(obj))
                    except git.GitCommandError:
                        pass
                return Response({'status': {"code": 1, "message": u"Данные сохранены"}}, status=status_codes.HTTP_200_OK)
            return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def delete(self, request, pk):
        status = {}
        obj = self.get_object()
        allowed_states = [
            Repository.NEW,
            Repository.LOADED,
            Repository.FAIL_LOAD,
            Repository.FAIL_UPDATE
        ]
        if not any([obj.state == allowed for allowed in allowed_states]):
            status["code"] = -1
            status["message"] = u"Невозможно удалить репозиторий"
        else:
            try:
                delete.delay(obj.id)
            except Exception as e:
                status["code"] = -2
                status["message"] = u"Ошибка при добавлении задачи"
                if settings.DEBUG:
                    print "Error while adding update task: ", str(e)
            else:
                status["code"] = 1
                status["message"] = u"Репозиторий будет удалён из списка сразу после того как будут удалены все файлы"
        return Response({'status': status}, status=status_codes.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)