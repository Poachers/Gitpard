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
import itertools as it


def format_delta(seconds):
    hours = seconds / 3600.0
    days = hours / 24.0
    mounts = days / (365.25 / 12)
    years = days / 365.25
    if years >= 1:
        years = int(years)
        odd = years % 100
        if odd in range(2, 5) + list(it.chain(*[range(i * 10 + 2, i * 10 + 5) for i in range(2, 10)])):
            return u"%s года" % years
        elif odd in [1, 21, 31, 41, 51, 61, 71, 81, 91]:
            return u"%s год" % years
        else:
            return u"%s лет" % years
    if mounts >= 1:
        mounts = int(mounts)
        odd = mounts % 100
        if odd == 1:
            return u"1 месяц"
        elif odd in [2, 3, 4]:
            return u"%s месяца" % mounts
        else:
            return u"%s месяцев" % mounts
    if days >= 1:
        days = int(days)
        odd = days % 100
        if odd in range(2, 5) + list(it.chain(*[range(i * 10 + 2, i * 10 + 5) for i in range(2, 10)])):
            return u"%s дня" % days
        elif odd in [1, 21, 31, 41, 51, 61, 71, 81, 91]:
            return u"%s день" % days
        else:
            return u"%s дней" % days
    if hours >= 1:
        hours = int(hours)
        odd = hours % 100
        if odd in [1, 21]:
            return u"1 час"
        elif odd in [2, 3, 4, 22, 23, 24]:
            return u"%s часа" % hours
        else:
            return u"%s часов" % hours
    return u"%s сек" % seconds


def create_report_path():
    # TODO указать формат файла
    uniq_file = str(uuid.uuid4())
    return os.path.join(settings.REPORT_ROOT, uniq_file)


def get_files(repo_id, branch, mask=None, *args, **kwargs):
    repo_obj = get_object_or_404(Repository, pk=repo_id)
    repo = git.Repo(repo_obj.path)
    try:
        repo.git.checkout(branch)
    except git.GitCommandError as e:
        if str(e).find("did not match any file(s) known to git"):
            raise Http404
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
    repo_obj = get_object_or_404(Repository, pk=repo_id, user=user)
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
