# coding: utf-8
import json

import os

import git
from Gitpard import settings
from rest_framework import viewsets, status as status_codes
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from Gitpard.apps.repository import serializers
from Gitpard.apps.repository.models import Repository
from Gitpard.apps.repository.helpers import get_url
from Gitpard.apps.repository.tasks import clone, update, delete


class RepositoryViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.RepositorySerializer
    queryset = Repository.objects

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_dict = serializer.data
        response_dict["log"] = json.loads(response_dict["log"])
        return Response(response_dict)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        serializer = self.get_serializer(queryset, many=True)

        response_dict = serializer.data
        for repo in response_dict:
            if repo["log"]:
                repo["log"] = json.loads(repo["log"])

        if page is not None:
            return self.get_paginated_response(response_dict)
        return Response(response_dict)

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
                obj.state = Repository.LOAD
                obj.save(update_fields=['state'])
                clone.delay(obj.id)
            except Exception as e:
                obj.state = Repository.FAIL_LOAD
                obj.save(update_fields=['state'])
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
                obj.state = Repository.UPDATE
                obj.save(update_fields=['state'])
                update.delay(obj.id)
            except Exception as e:
                obj.state = Repository.FAIL_UPDATE
                obj.save(update_fields=['state'])
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
                obj.state = Repository.BLOCKED
                obj.save(update_fields=['state'])
                delete.delay(obj.id)
            except Exception as e:
                status["code"] = -2
                status["message"] = u"Ошибка при добавлении задачи"
                if settings.DEBUG:
                    print "Error while adding delete task: ", str(e)
            else:
                status["code"] = 1
                status["message"] = u"Репозиторий будет удалён из списка, сразу после того как будут удалены все файлы"
        return Response({'status': status})

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)