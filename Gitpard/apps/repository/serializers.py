# -*- coding: utf-8 -*-
import re

from rest_framework import serializers

from Gitpard.apps.repository import models


class RepositorySerializer(serializers.ModelSerializer):
    """Сериализатор модели репозитория."""

    class Meta:
        model = models.Repository
        fields = ('id', 'url', 'login', 'password', 'name', 'kind', 'user', 'state', 'path', 'last_modify')

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
