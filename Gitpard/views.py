# coding: utf-8
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response, render


# TODO Вынести это из корня проекта
@login_required(login_url='/index')
def time(request):
    return render(request, 'repo_list.html')


def index(request):
    """
    :param request:
    :return: index page
    """
    return render(request, 'index.html')
