# coding: utf-8
import errno
import shutil

import os
import git
import stat
from django.http import Http404
from rest_framework import viewsets, status as status_codes, exceptions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.utils import timezone
from Gitpard.apps.repository import serializers
from Gitpard.apps.repository.models import Repository
from Gitpard.apps.repository.helpers import _get_url, get_pure_url
from Gitpard.apps.repository.tasks import clone, update, delete

class RepositoryViewSet(viewsets.ModelViewSet):
    """Viewset на основе сериализатора модели репозитория."""
    serializer_class = serializers.RepositorySerializer
    queryset = Repository.objects

    def _clone_repo(self):
        """Клонирование репозитория"""
        obj = self.get_object()
        status = {}
        clone.delay(obj.id)
        status["code"] = 7
        status["message"] = u"Подготовка к клонированию"
        return status

    def _update_repo(self):
        """Обновление репозитория"""
        obj = self.get_object()
        status = {}
        update.delay(obj.id)
        status["code"] = 7
        status["message"] = u"Подготовка к обновлению"
        return status

    def _delete_repo(self):
        obj = self.get_object()
        status = {}
        """Асинхронный метод удаления"""
        delete.delay(obj.id)
        status["code"] = 7
        status["message"] = u"Подготовка к удалению"

    @detail_route(methods=['get'])
    def clone(self, request, pk):
        """Rest метод запуска механизма клонирования репозитория."""
        status = self._clone_repo()
        return Response({'status': status}, status=status_codes.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='update')
    def update_repo(self, request, pk):
        """Rest метод запуска механизма обновления репозитория."""
        obj = self.get_object()
        if not obj:
            raise exceptions.NotFound
        status = self._update_repo()
        return Response({'status': status}, status=status_codes.HTTP_200_OK)

    @detail_route(methods=['get', 'post'])
    def edit(self, request, pk):
        """Rest метод редактирования репозитория"""
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
                    repo = git.Repo.init(obj.path)
                    if repo.remote('origin') in repo.remotes:
                        repo.git.remote("set-url", "origin", _get_url(obj))
                return Response({'status': {"code": 1, "message": u"Данные сохранены"}}, status=status_codes.HTTP_200_OK)
            return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def delete(self, request, pk):
        """Rest метод удаления репозитория"""
        status = self._delete_repo()
        return Response({'status': status}, status=status_codes.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)