# coding: utf-8

# Core
import os
from urlparse import urlparse
import uuid
# Vendor

# Project
from Gitpard import settings


def create_repo_path():
    """Генерирует уникальный путь до репозитория. Но не cоздает ее."""
    uniq_dir = str(uuid.uuid4())
    return os.path.join(settings.REPO_ROOT, uniq_dir)

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
