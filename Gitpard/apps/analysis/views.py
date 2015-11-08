# coding: utf-8
import os
from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from Gitpard.apps.repository.models import Repository
import git
import json


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

    def fileInRepo(repo, filePath):
        """
        repo is a gitPython Repo object
        filePath is the full path to the file from the repository root
        returns true if file is found in the repo at the specified path, false otherwise
        """
        pathdir = os.path.dirname(filePath)

        #Build up reference to desired repo path
        rsub = repo.head.commit.tree

        for path_element in pathdir.split(os.path.sep):

            # If dir on file path is not in repo, neither is file.
            try :
                rsub = rsub[path_element]

            except KeyError :

                return False

        return(filePath in rsub)
    try:
        repo.git.checkout(branch)
        temp = []
        if fileInRepo(repo, file_path):
            for index, commit in enumerate(repo.blame(branch, file_path), start=1):
                temp.append({
                    "number": index,
                    "line": commit[1][0],
                    "author": commit[0].author.name,
                    "created_date": datetime.datetime.fromtimestamp(commit[0].authored_date).strftime('%Y-%m-%d %H:%M:%S'),
                    "commit": commit[0].hexsha})
            return json.dumps({'data': temp})
        else:
            return json.dumps({'error': 'file not found'})

    except git.GitCommandError as e:
        if str(e).find("did not match any file(s) known to git"):
            raise Http404
