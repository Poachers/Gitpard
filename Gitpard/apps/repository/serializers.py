# coding: utf-8

import re
from Gitpard import settings
from Gitpard.apps.repository.helpers import get_pure_url
from django.utils import timezone
from rest_framework import serializers
import git
from Gitpard.apps.repository import models, helpers


class RepositorySerializer(serializers.ModelSerializer):
    """Сериализатор модели репозитория."""

    def create(self, validated_data):
        """
        Дополняем данные о репозитории требуемой доп. информацией.
        Такой как путь хранения, кем добавлени, и логируем дату и время.
        """
        name = validated_data.get('name')
        validated_data.update({
            'user': self.context['request'].user,
            'path': helpers.create_repo_path(),
            'last_modify': timezone.now(),
            'name': name,
        })
        return super(RepositorySerializer, self).create(validated_data)

    def validate_name(self, name):
        if not name:
            raise serializers.ValidationError(u"Введите имя репозитория")
        return name

    def validate_url(self, url):
        """Проверка на соответствие паттерну ссылки репозитория.
         Пока поддерживам только http и https.

        :param url: урл для загрузки репозитория
        """
        git_url = re.compile(r'^(https|http)://([\w\.@:/\-~]+)(\.git)$')
        if not git_url.match(url):
            raise serializers.ValidationError(u"Некорректный url репозитория")
        url = get_pure_url(url)
        try:
            try:
                url_elements = url.split("/")
                protocol = url_elements[0]
                domain_name = url_elements[2].split('@')[-1]
                owner_name = url_elements[3]
                repo_name = url_elements[4]
                login = self.context["request"].data["login"]
                password = self.context["request"].data["password"]
                elements = {
                    "protocol": protocol,
                    "login": login,
                    "password": password,
                    "domain_name": domain_name,
                    "owner_name": owner_name,
                    "repo_name": repo_name
                }
                # даже если подавать utf строчку, выдаст ошибку, т.к. utf не поддерживается в библиотеке gitpython
                # поэтому просто отлавливаем ошибку
                git.Git().ls_remote(
                    "{protocol}//{login}:{password}@{domain_name}/{owner_name}/{repo_name}".format(**elements))
            except git.GitCommandError as ge:
                print ge
                if "not found" in str(ge):
                    error = {"code": -1, "message": u"Удалённый репозиторий не найден"}
                elif "Authentication failed" in str(ge):
                    error = {"code": -1, "message": u"Неверный логин или пароль"}
                else:
                    error = {"code": -1, "message": u"Удалённый репозиторий недоступен"}
                    if settings.DEBUG:
                        print "Repository checking error: ", str(ge)
                raise serializers.ValidationError(error)
            except KeyError:
                raise serializers.ValidationError(u"Заполните все данные")
            except UnicodeDecodeError:
                raise serializers.ValidationError(u"Пожалуйста используйте только ASCII символы.")
            except UnicodeEncodeError:
                raise serializers.ValidationError(u"Пожалуйста используйте только ASCII символы")
            prev = models.Repository.objects.get(url=url, user=self.context['request'].user)
        except models.Repository.DoesNotExist:
            pass
        else:
            if "pk" in self.context:
                if models.Repository.objects.get(pk=int(self.context["pk"])).url == url:
                    return url
            raise serializers.ValidationError(u"Текущий репозиторий уже добавлен под названием %s" % prev.name)
        return url

    class Meta:
        model = models.Repository
        fields = ('id', 'url', 'login', 'password', 'name',
                  'kind', 'state', 'last_modify', 'log')
        read_only_fields = ('user', 'state', 'last_modify', 'log')
        extra_kwargs = {'password': {'write_only': True}}


class RepositoryEditSerializer(RepositorySerializer):
    class Meta:
        model = models.Repository
        fields = ('id', 'url', 'login', 'password', 'name',
                  'kind', 'state', 'last_modify')
        read_only_fields = ('url', 'user', 'state', 'last_modify')
        extra_kwargs = {'password': {'write_only': True}}
