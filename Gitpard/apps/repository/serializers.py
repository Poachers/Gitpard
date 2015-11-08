# coding: utf-8

import re
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
            raise serializers.ValidationError(u"Заполните поле")
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
            # try:
            #     git.Git().ls_remote(url)
            # except git.GitCommandError as e:
            #     raise serializers.ValidationError(u"Данный репозиторий не найден")
            prev = models.Repository.objects.get(url=url, user=self.context['request'].user)
        except models.Repository.DoesNotExist:
            pass
        else:
            if "pk" in self.context:
                if models.Repository.objects.get(pk=int(self.context["pk"])).url == url:
                    return url
            raise serializers.ValidationError(u"Репозиторий уже существует под названием %s" % prev.name)
        return url

    class Meta:
        model = models.Repository
        fields = ('id', 'url', 'login', 'password', 'name',
                  'kind', 'state', 'last_modify')
        read_only_fields = ('user', 'state', 'last_modify')
        extra_kwargs = {'password': {'write_only': True}}


class RepositoryEditSerializer(RepositorySerializer):

    class Meta:
        model = models.Repository
        fields = ('id', 'url', 'login', 'password', 'name',
                  'kind', 'state', 'last_modify')
        read_only_fields = ('url', 'user', 'state', 'last_modify')
        extra_kwargs = {'password': {'write_only': True}}
