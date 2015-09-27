# coding: utf-8

import re

from django.utils import timezone
from rest_framework import serializers

from Gitpard.apps.repository import models, helpers


class RepositorySerializer(serializers.ModelSerializer):
    """Сериализатор модели репозитория."""

    def create(self, validated_data):
        """
        Дополняем данные о репозитории требуемой доп. информацией.
         Такой как путь хранения, кем добавлени, и логируем дату и время.
        """
        name = validated_data.get('name')
        print '>>>>>', self.context['request'].user
        if not name:
            name = helpers.create_name_by_url(validated_data.get('url'))
        validated_data.update({
            'user': self.context['request'].user,
            'path': helpers.create_repo_path(),
            'last_modify': timezone.now(),
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

    class Meta:
        model = models.Repository
        fields = ('id', 'url', 'login', 'password', 'name',
                  'kind', 'state', 'last_modify')
        read_only_fields = ('user', 'state', 'last_modify')
