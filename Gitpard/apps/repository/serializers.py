# -*- coding: utf-8 -*-
import os
import datetime
import re
import uuid

from rest_framework import serializers
from Gitpard import settings

from Gitpard.apps.repository import models
from Gitpard.apps.repository.helpers import create_repo_path, create_name_by_url


class RepositorySerializer(serializers.ModelSerializer):
    """Сериализатор модели репозитория."""

    class Meta:
        model = models.Repository
        fields = ('id', 'url', 'login', 'password', 'name',
                  'kind', 'user', 'state', 'last_modify')
        read_only_fields = ('user', 'state', 'last_modify')

    def create(self, validated_data):
        """
        Дополняем данные о репозитории требуемой доп. информацией.
         Такой как путь хранения, кем добавлени, и логируем дату и время.
        """
        name = validated_data.get('name')
        if not name:
            name = create_name_by_url(validated_data.get('url'))
        validated_data.update({
            'user': self.context['request'].user,
            'path': create_repo_path(),
            'last_modify': datetime.datetime.now(),
            'name': name,
        })
        return super(RepositorySerializer, self).create(validated_data)

    def validate_url(self, url):
        """Проверка на соответствие паттерну ссылки репозитория.
         Пока поддерживам только http и https.

        :param url: урл для загрузки репозитория
        """
        git_url = re.compile(r'^(https|http)://([\w\.@:/\-~]+)(\.git)$')
        if not git_url.match(url):
            raise serializers.ValidationError(
                u"Некорректный урл репозитория. "
                u"Корректным считается только http/https урл.")

        return url
