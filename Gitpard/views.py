# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from subprocess import Popen, PIPE


# TODO Вынести это из корня проекта
from django.template import RequestContext


@login_required(login_url='/index')
def repos_list(request):
    return render(request, 'reposList/index.html')


@login_required(login_url='/index')
def analysis(request):
    return render_to_response('analysis.html', RequestContext(request))


@login_required(login_url='/index')
def report_file(request):
    return render_to_response('report_file.html', RequestContext(request))
    # return render(request, 'analysis.html')

def upload_repo(request):
    html = 'sh update.sh;'
    ugit = '</br>'.join(Popen(html, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().split('\n'))
    return HttpResponse(ugit, content_type='text/html')


def index(request):
    """
    :param request:
    :return: index page
    """
    return render(request, 'index.html')


@login_required(login_url='/index')
def report(request):
    return render(request, 'report/index.html')


@login_required(login_url='/index')
def report_new(request):
    return render(request, 'report/new.html')


@login_required(login_url='/index')
def report_view(request):
    return render(request, 'report/view.html')
