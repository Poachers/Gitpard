# -*- coding: utf-8 -*-
import uuid

from django.conf import settings

from rest_framework import viewsets

from Gitpard.apps.repository import serializers, models


class RepositoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RepositorySerializer
    queryset = models.Repository.objects

    def get_queryset(self):
        return models.Repository.objects.filter(user=self.request.user)
