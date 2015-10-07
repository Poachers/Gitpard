# coding: utf-8

import os

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
        status = ""
        if not (obj.state == Repository.NEW or
                obj.state == Repository.FAIL_LOAD):
            #raise exceptions.NotFound
            status = u"Репозиторий уже был склонирован"
            return status
        try:
            git.Repo.clone_from(obj.url, obj.path)
            obj.state = Repository.LOADED
            status = u"Репозиторий успешно клонирован"
        except git.GitCommandError:
            if os.path.exists(obj.path):
                os.rmdir(obj.path)
            obj.state = Repository.FAIL_LOAD
            #raise exceptions.ValidationError(
            #    detail=u'Что-то пошло не так.Возможно урл репозитория'
            #           u'не действительный или есть проблемы с доступом')
            status = u"Ошибка при клонировании репозитория"
        finally:
            obj.last_modify = timezone.now()
            obj.save()
            return status

    def _update_repo(self):
        #TODO реализовать обновление репозитория
        return u"Репозиторий успешно обновлён"

    def _delete_repo(self):
        #TODO реализовать удаление папки с репозиторием
        obj = self.get_object()
        obj.delete()
        return u"Репозиторий успешно удалён"

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
        self.serializer_class = serializers.RepositoryEditSerializer
        obj = self.get_object()
        if request.method == 'GET':
            serializer = serializers.RepositoryEditSerializer(obj)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = serializers.RepositoryEditSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': u"Данные сохранены"}, status=status_codes.HTTP_200_OK)
            return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def delete(self, request, pk):
        """Rest метод удаления репозитория"""
        status = self._delete_repo()
        return Response({'status': status}, status=status_codes.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)
