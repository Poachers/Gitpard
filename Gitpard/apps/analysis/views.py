# coding: utf-8
import os
from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from Gitpard.apps.repository.models import Repository
import git


@api_view(['GET'])
def branches(request, repo_id, *args, **kwargs):
    repo_obj = get_object_or_404(Repository, pk=repo_id)
    repo = git.Repo(repo_obj.path)
    branches = [{"branch_name": r.name} for r in repo.heads]
    return Response({"branches": branches})


@api_view(['GET'])
def branch_tree(request, repo_id, branch, *args, **kwargs):
    repo_obj = get_object_or_404(Repository, pk=repo_id)
    repo = git.Repo(repo_obj.path)
    try:
        repo.git.checkout(branch)
    except git.GitCommandError as e:
        if str(e).find("did not match any file(s) known to git"):
            raise Http404
    tree = {}

    def get_elem(d, l):  # Функция возвращает элемент из словаря по списку ключей
        for item in l:
            d = d[item]
        return d

    for d, dirs, files in os.walk(repo_obj.path):
        path = d.replace(repo_obj.path, "", 1).split("\\")  # Путь до текущей папки в виде списка
        if ".git" in path:
            continue
        try:
            directory = get_elem(tree, path)  # Получаем словарь для этой папки
        except KeyError:  # Если для этой папки ещё не создан словарь создаём его
            get_elem(tree, path[:-1])[path[-1:][0]] = {}
            directory = get_elem(tree, path)
        for file in files:  # Помещаем файлы в словарь
            directory[file] = "file"

    return Response({"repo_name": repo_obj.name, "branch_name": branch, "project": tree[""]})