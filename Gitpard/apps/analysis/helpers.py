# coding: utf-8
import uuid

import itertools

import os
import re
import git
from Gitpard import settings
from Gitpard.apps.repository.models import Repository
from django.http import Http404
from django.shortcuts import get_object_or_404


def create_report_path():
    # TODO указать формат файла
    uniq_file = str(uuid.uuid4())
    return os.path.join(settings.REPORT_ROOT, uniq_file)


def get_files(repo_id, branch, mask=None, *args, **kwargs):
    # repo_obj = get_object_or_404(Repository, pk=repo_id)
    repo_obj = Repository.objects.get(pk=repo_id)
    repo = git.Repo(repo_obj.path)
    #try:
    #    repo.git.checkout(branch)
    #except git.GitCommandError as e:
    #    if str(e).find("did not match any file(s) known to git"):
    #        raise Http404

    repo.git.checkout(branch)
    if mask:
        try:
            include_list = itertools.compress(mask['include'], mask['include'])
            exclude_list = itertools.compress(mask['exclude'], mask['exclude'])
            include = [re.compile(regex) for regex in include_list]
            exclude = [re.compile(regex) for regex in exclude_list]
        except re.error:
            raise ValueError(u"Ошибка при парсинге регулярных выражений")
        except KeyError:
            raise ValueError(u"Неверный формат маски")
    else:
        include, exclude = [], []

    list_of_files = []
    for current, dirs, files in os.walk(repo_obj.path):
        total_path = current.replace(repo_obj.path, "", 1)
        path, dir = os.path.split(total_path)
        folders = []
        while dir:
            folders.append(dir)
            path, dir = os.path.split(path)
        folders.reverse()
        if folders:
            total_path = total_path[1:]
        if ".git" in folders:
            continue
        for file in files:
            path = os.path.join(total_path, file)
            file_mask = True
            if include:
                file_mask = True
                for include_re in include:
                    if include_re.search(path):
                        break
                else:
                    file_mask = False
            if exclude:
                file_include = file_mask
                file_mask = False
                for exclude_re in exclude:
                    if exclude_re.search(path):
                        break
                else:
                    file_mask = True and file_include
            if file_mask:
                list_of_files.append(path)
    if mask and not list_of_files:
        raise ValueError(u"Ни один файл не удовлетворяет маске")
    return list_of_files


def get_tree(repo_id, branch, user, mask=None, *args, **kwargs):
    repo_obj = get_object_or_404(Repository, pk=repo_id)
    repo = git.Repo(repo_obj.path)
    try:
        repo.git.checkout(branch)
    except git.GitCommandError as e:
        e.message = branch
        raise e

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
        if folders:
            total_path = total_path[1:]
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
            path = os.path.join(total_path, file)
            if mask:
                file = {
                    "text": file,
                    "selectable": False,
                    "color": "#000" if path in mask else "#ccc"
                }
            else:
                file = {
                    "text": file,
                    "selectable": True
                }
            folder["nodes"].append(file)

    return {"repo_name": repo_obj.name, "branch_name": branch, "project": files_tree["nodes"]}
