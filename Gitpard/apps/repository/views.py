# coding: utf-8

# Vendor
import git
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound
# Project
from Gitpard.apps.repository import serializers
from Gitpard.apps.repository.models import Repository


class RepositoryViewSet(viewsets.ModelViewSet):
    """Viewset на основе сериализатора модели репозитория."""
    serializer_class = serializers.RepositorySerializer
    queryset = Repository.objects

    @detail_route(methods=['get'])
    def clone_repository(self, request, pk):
        try:
            repository = Repository.get(pk=pk)
            if (repository.state == Repository.NEW or
                repository.state == Repository.FAIL_LOAD):
                git.Repo.clone_from(uploading_url, repo_path)
                utils.update_repo_branches(repo_path, uploading_url)


        except Repository.DoesNotExist:
            raise NotFound(detail="Repository doesn't exist")

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)
