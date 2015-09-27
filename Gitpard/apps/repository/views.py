# coding: utf-8

import os
from urlparse import urlparse

import git
from rest_framework import viewsets, status as status_codes, exceptions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.utils import timezone

from Gitpard.apps.repository import serializers
from Gitpard.apps.repository.models import Repository


class RepositoryViewSet(viewsets.ModelViewSet):
    """Viewset на основе сериализатора модели репозитория."""
    serializer_class = serializers.RepositorySerializer
    queryset = Repository.objects


    @staticmethod
    def _get_url(obj):
        # TODO нужна нормальная проработанная реализация
        # для приватных репозиториев
        if obj.kind == Repository.PRIVATE:
            raise NotImplemented

        return obj.url

    def _clone_repo(self):
        """Клонирование репозитория"""
        obj = self.get_object()
        if not (obj.state == Repository.NEW or
                obj.state == Repository.FAIL_LOAD):
            raise exceptions.NotFound
        try:
            git.Repo.clone_from(obj.url, obj.path)
            obj.state = Repository.LOADED
        except git.GitCommandError:
            if os.path.exists(obj.path):
                os.rmdir(obj.path)
            obj.state = Repository.FAIL_LOAD
            raise exceptions.ValidationError(
                detail=u'Что-то пошло не так.Возможно урл репозитория'
                       u'не действительный или есть проблемы с доступом')
        finally:
            obj.last_modify = timezone.now()
            obj.save()

    @detail_route(methods=['get'])
    def clone(self, request, pk):
        """Rest метод запуска механизма клонирования репозитория."""
        self._clone_repo()
        return Response(status=status_codes.HTTP_200_OK)

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)
