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
                if node["name"] == elem and node["type"] == "folder":
                    tree = node
                    break
        return tree

    files_tree = {
        "name": "root",
        "type": "folder",
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
                "name": dir,
                "type": "folder",
                "nodes": []
            }
            folder["nodes"].append(dir)

        for file in files:
            file = {
                "name": file,
                "type": "file"
            }
            folder["nodes"].append(file)

    return Response({"repo_name": repo_obj.name, "branch_name": branch, "project": files_tree["nodes"]})