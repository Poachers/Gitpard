import Gitpard.apps.analysis.views as views
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^analysis/$', login_required(views.branches), name='repo_branches'),
    url(r'^analysis/(?P<branch>.+)$', login_required(views.branch_tree), name='files_tree'),
)

urlpatterns = format_suffix_patterns(urlpatterns)