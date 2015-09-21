# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .api import get_api_urls

urlpatterns = [
    url(r'^api/', include(get_api_urls())),
    url(r'^admin/', include(admin.site.urls)),
]
