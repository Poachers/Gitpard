# coding: utf-8
import Gitpard
import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from Gitpard.views import time, index, analysis, report, upload_repo
from .api import get_api_urls

urlpatterns = [
    url(r'^api/', include(get_api_urls(), namespace='api')),
    url(r'^api/repositories/(?P<repo_id>\d+)/', include(Gitpard.apps.analysis.urls)),
    url(r'^$', time),
    url(r'^index$', index),
    url("^auth/", include("social.apps.django_app.urls", namespace="social")),
    url(r'^auth/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^analysis/', analysis),
    url(r'^upload/', upload_repo),
    url(r'^report/', report),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG is False:   # if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )