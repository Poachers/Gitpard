import Gitpard.apps.analysis.views as views
from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

report_router = routers.DefaultRouter()
report_router.register(r'report', views.ReportViewSet)

urlpatterns = patterns('',
    url(r'^analysis/$', login_required(views.branches), name='repo_branches'),
    url(r'^analysis/(?P<branch>[^/]+)/$', login_required(views.branch_tree), name='files_tree'),
    url(r'^report/tree$', login_required(views.masked_branch_tree), name='masked_files_tree'),
    url(r'^analysis/(?P<branch>[^/]+)/(?P<file_path>.+)$', login_required(views.annotation_file), name='annotation_file'),
    url(r'^history/(?P<ts>[0-9]+)/(?P<total>[0-1].)/(?P<module>[0-9]+)$', login_required(views.repo_history), name='repo_history'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns.append(url(r'^', include(report_router.urls)))