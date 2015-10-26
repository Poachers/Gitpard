# coding: utf-8

# Core
import os
from urlparse import urlparse
import uuid
# Vendor

# Project
from Gitpard import settings
from Gitpard.apps.repository.models import Repository


def create_repo_path():
    """Генерирует уникальный путь до репозитория. Но не cоздает ее."""
    uniq_dir = str(uuid.uuid4())
    return os.path.join(settings.REPO_ROOT, uniq_dir)

def _get_url(obj):
        """Конструктор url для работы с удалённым репозиторием"""
        url = obj.url
        url_elements = url.split("/")[2:]
        domain_name = url_elements[0].split('@')[-1]
        owner_name = url_elements[1]
        repo_name = url_elements[2]

        if obj.kind == Repository.PRIVATE:
            login = obj.login
            password = obj.password
            url = "https://%s:%s@%s/%s/%s" % (login, password, domain_name, owner_name, repo_name)
            return url

        elif obj.kind == Repository.PUBLIC:
            url = "https://%s:%s@%s/%s/%s" % ("", "", domain_name, owner_name, repo_name)
            return url

def create_name_by_url(url):
    """
    Извлекает название проекта по умолчанию из  урл.
     ссылка вида http://...../user(or team)/project_name.git;

    Example:
        input: https://bitbucket.org/poachers/gitpard.git
        result: poachers gitpard
    """
    purl = urlparse(url)
    return " ".join(os.path.splitext(purl.path)[0].split('/')[1:])
