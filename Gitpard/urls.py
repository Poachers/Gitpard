# coding: utf-8

from django.conf.urls import include, url
from django.contrib import admin
from Gitpard.views import time, index
from .api import get_api_urls

urlpatterns = [
    url(r'^api/', include(get_api_urls(), namespace='api')),
    url(r'^$', time),
    url(r'^index$', index),
    url("^auth/", include("social.apps.django_app.urls", namespace="social")),
    url(r'^auth/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^admin/', include(admin.site.urls)),
]
