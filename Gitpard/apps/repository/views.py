# coding: utf-8
import datetime

import os
import shutil

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
        """Конструктор url для работы с удалённым репозиторием"""
        if obj.kind == Repository.PRIVATE:
            url = obj.url
            login = obj.login
            password = obj.password

            url_elements = url.split("/")[2:]
            domain_name = url_elements[0].split('@')[-1]
            owner_name = url_elements[1]
            repo_name = url_elements[2]

            url = "https://%s:%s@%s/%s/%s" % (login, password, domain_name, owner_name, repo_name)

            return url

        elif obj.kind == Repository.PUBLIC:
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
            git.Repo.clone_from(self._get_url(obj), obj.path)
            obj.state = Repository.LOADED
            status = u"Репозиторий успешно клонирован"
        except git.GitCommandError as e:
            if os.path.exists(obj.path):
                os.rmdir(obj.path)
            obj.state = Repository.FAIL_LOAD
            #raise exceptions.ValidationError(
            #    detail=u'Что-то пошло не так.Возможно урл репозитория'
            #           u'не действительный или есть проблемы с доступом')
            status = u"Ошибка при клонировании репозитория" + str(e)
        except Exception as e:
            obj.state = Repository.FAIL_UPDATE
            status = u"Ошибка при клонировании репозитория: " + str(e)
        finally:
            obj.last_modify = timezone.now()
            obj.save()
            return status

    def _update_repo(self):
        """Обновление репозитория"""
        obj = self.get_object()
        status = ""
        if not (obj.state == Repository.LOADED or
                obj.state == Repository.FAIL_UPDATE):
            status = u"Репозиторий не клонирован"
            return status
        try:
            repo = git.Repo.init(obj.path)
            origin = repo.remote('origin')
            repo.git.execute("git fetch")  # Делаем fetch чтобы получить удалённые ветки
            for ref in origin.refs[1:]:  # Пробегаемся по веткам и делаем pull
                repo.git.execute("git reset --merge")
                repo.git.execute("git checkout %s" % ref.remote_head)
                repo.git.execute("git pull origin %s" % ref.remote_head)
            status = u"Репозиторий успешно обновлён"
        except git.GitCommandError as e:
            obj.state = Repository.FAIL_UPDATE
            status = u"Ошибка при обновлении репозитория: " + str(e)
        except Exception as e:
            obj.state = Repository.FAIL_UPDATE
            status = u"Ошибка при обновлении репозитория: " + str(e)
        finally:
            obj.last_modify = timezone.now()
            obj.save()
            return status

    def _delete_repo(self):
        """Удаление репозитория"""
        obj = self.get_object()
        if os.path.exists(obj.path):
            shutil.rmtree(obj.path, ignore_errors=True)
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
