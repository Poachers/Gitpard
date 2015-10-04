# -*- coding: utf-8 -*-
from django.conf.urls import include

URL_PATTERNS = (
    'Gitpard.apps.repository.urls',
)


def get_api_urls():
    result = []
    for module, _, _ in map(include, URL_PATTERNS):
        if hasattr(module, 'router'):
            result.extend(module.router.urls)

    return result
