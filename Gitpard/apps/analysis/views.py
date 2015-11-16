# coding: utf-8
import os
import git
import datetime
import json
from django.http import Http404
from django.utils.safestring import mark_safe
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from Gitpard.apps.repository.models import Repository


@api_view(['GET'])
def branches(request, repo_id, *args, **kwargs):
    repo_obj = get_object_or_404(Repository, pk=repo_id, user=request.user)
    repo = git.Repo(repo_obj.path)
    branches = [{"branch_name": r.name} for r in repo.heads]
    return Response({"branches": branches})


@api_view(['GET'])
def branch_tree(request, repo_id, branch, *args, **kwargs):
    repo_obj = get_object_or_404(Repository, pk=repo_id, user=request.user)
    repo = git.Repo(repo_obj.path)
    try:
        repo.git.checkout(branch)
    except git.GitCommandError as e:
        if str(e).find("did not match any file(s) known to git"):
            raise Http404

    def get_folder(tree, list):
        for elem in list:
            for node in tree["nodes"]:
                if node["text"] == elem and node["selectable"] == False:
                    tree = node
                    break
        return tree

    files_tree = {
        "text": "root",
        "selectable": False,
        "nodes": []
    }

    for current, dirs, files in os.walk(repo_obj.path):
        total_path = current.replace(repo_obj.path, "", 1)
        path, dir = os.path.split(total_path)
        folders = []
        while dir:
            folders.append(dir)
            path, dir = os.path.split(path)
        folders.reverse()

        if ".git" in folders:
            continue

        folder = get_folder(files_tree, folders)
        for dir in dirs:
            if dir == ".git":
                continue
            dir = {
                "text": dir,
                "selectable": False,
                "nodes": []
            }
            folder["nodes"].append(dir)

        for file in files:
            file = {
                "text": file,
                "selectable": True
            }
            folder["nodes"].append(file)

    return Response({"repo_name": repo_obj.name, "branch_name": branch, "project": files_tree["nodes"]})


@api_view(['GET'])
def annotation_file(request, repo_id, branch, file_path, *args, **kwargs):
    """
    :param request:
    :param repo_id: int
    :param branch: string
    :param file_path: string
    :param args:
    :param kwargs:
    :return: json
    """
    repo_obj = get_object_or_404(Repository, pk=repo_id, user=request.user)
    repo = git.Repo(repo_obj.path)
    try:
        repo.git.checkout(branch)
        temp = []
        index = 1
        for commit, lines in repo.blame(branch, file_path):
            for line in lines:
                temp.append({
                    "number": index,
                    "line": line,
                    "author": commit.author.name,
                    "created_date": datetime.datetime.fromtimestamp(commit.authored_date),
                    "commit": commit.hexsha})
                index += 1
        return Response({'data': temp})
    except git.GitCommandError:
        res = {"error":
                   {"code": 403,
                    "message": "Bad Requset",
                    "description": "did not match any file(s) known to git"}
               }
        return Response(data=res, status='403')
