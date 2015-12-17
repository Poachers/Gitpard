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
    return render_to_response('analysis.html',RequestContext(request))

@login_required(login_url='/index')
def report_author(request):
    return render_to_response('report_author.html',RequestContext(request))

@login_required(login_url='/index')
def report_file(request):
    return render_to_response('report_file.html',RequestContext(request))
    # return render(request, 'analysis.html')

def upload_repo(request):
    href_commits = 'https://bitbucket.org/poachers/gitpard/commits/'
    href_issues = 'https:\/\/bitbucket.org\/poachers\/gitpard\/issues\/'
    html =  'echo "<code>===============================";' \
            'echo "========== git pull ===========";' \
            'echo "===============================</br>";' \
            'git pull;' \
            'echo;' \
            'git log -1 --pretty=format:"<a href="' + href_commits + '%H">%h</a>: ";' \
            'git log -1 --pretty=format:"%s" | sed \'s/\(#\([1-9][0-9]*\)\)\(.*\)/<a href="' + href_issues + '\\2">\\1<\/a>\\3/g\';' \
            'git log -1 --pretty=format:"</br>%ar</br>%an &lt;%ce&gt;</br></br>";' \
            'echo "===============================";' \
            'echo "===== ./manage.py migrate =====";' \
            'echo "===============================</br>";' \
            ' ./manage.py migrate;' \
            'echo "</code>";'
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
