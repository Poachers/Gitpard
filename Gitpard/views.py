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
def time(request):
    return render(request, 'repo_list.html')


@login_required(login_url='/index')
def analysis(request):
    return render_to_response('analysis.html',RequestContext(request))
    # return render(request, 'analysis.html')

def upload_repo(request):
    print Popen('echo $PWD', shell=True, stdout=True)
    return HttpResponse(Popen("cat ~/.ssh/id_rsa.pub", shell=True, stdin=PIPE, stdout=PIPE).stdout.read().split(), content_type='application/json')

def index(request):
    """
    :param request:
    :return: index page
    """
    return render(request, 'index.html')

@login_required(login_url='/index')
def report(request):
    return render(request, 'report/index.html')
