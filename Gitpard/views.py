# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render_to_response, render


# TODO Вынести это из корня проекта
@login_required(login_url='/index')
def time(request):
    return render(request, 'repo_list.html')


@login_required(login_url='/index')
def analysis(request):
    file_html = open(settings.BASE_DIR + '/Gitpard/apps/repository/views.py')
    file = []
    for i in file_html.readlines():
        file.append(dict(num=len(file), title=i, a='guy-full-in', date='4.10.2015', com='fix fix fix fix fix fix fix fix fix'))
    file_html.close()
    return render_to_response('analysis.html', {'file': file})
    # return render(request, 'analysis.html')


def index(request):
    """
    :param request:
    :return: index page
    """
    return render(request, 'index.html')
