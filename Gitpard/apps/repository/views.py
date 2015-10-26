# coding: utf-8
import errno
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
from Gitpard.apps.repository.helpers import _get_url
from Gitpard.apps.repository.tasks import clone, update, delete

class RepositoryViewSet(viewsets.ModelViewSet):
    """Viewset на основе сериализатора модели репозитория."""
    serializer_class = serializers.RepositorySerializer
    queryset = Repository.objects

    def _clone_repo(self):
        """Клонирование репозитория"""
        obj = self.get_object()
        status = {}
        if not (obj.state == Repository.NEW or
                obj.state == Repository.FAIL_LOAD):
            status["code"] = -1
            status["message"] = u"Репозиторий уже был склонирован"
            return status
        try:
            obj.state = Repository.LOAD
            obj.save()
            """Асинхронный метод клонирования"""
            clone.delay(obj.id)
            status["code"] = 5
            status["message"] = u"Репозиторий клонируется"
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

    def _update_repo(self):
        """Обновление репозитория"""
        obj = self.get_object()
        status = {}
        if not (obj.state == Repository.LOADED or
                obj.state == Repository.FAIL_UPDATE):
            status["code"] = -1
            status["message"] = u"Репозиторий не был склонирован"
            return status
        try:
            obj.state = Repository.UPDATE
            obj.save()
            """Асинхронный метод обновления"""
            update.delay(obj.id)
            status["code"] = 5
            status["message"] = u"Репозиторий обновляется"
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
                status["message"] = u"Ошибка сервера"
        except Exception as e:
            obj.state = Repository.FAIL_UPDATE
            print "Update error: " + str(e)
            status["code"] = -4
            status["message"] = u"Ошибка сервера"
        finally:
            obj.last_modify = timezone.now()
            obj.save()
            return status

    def _delete_repo(self):
        """Удаление репозитория"""
        obj = self.get_object()
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

        obj = self.get_object()
        if os.path.exists(obj.path):
            shutil.rmtree(obj.path, ignore_errors=False, onerror=handle_remove_readonly)
        """Асинхронный метод удаления"""
        delete.delay(obj.id)
        status["code"] = 5
        status["message"] = u"Репозиторий удаляется"
        return status

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
            serializer = serializers.RepositoryEditSerializer(obj)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = serializers.RepositoryEditSerializer(obj, data=request.data)
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