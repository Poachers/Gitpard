# -*- coding: utf-8 -*-
from rest_framework import viewsets

from Gitpard.apps.repository import serializers, models


class RepositoryViewSet(viewsets.ModelViewSet):
    """Viewset на основе сериализатора модели репозитория."""
    serializer_class = serializers.RepositorySerializer
    queryset = models.Repository.objects

    def get_queryset(self):
        return models.Repository.objects.filter(user=self.request.user)
