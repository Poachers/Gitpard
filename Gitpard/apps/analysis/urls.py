from rest_framework import routers

from Gitpard.apps.analysis import views

router = routers.DefaultRouter()
router.register(r'analysis', views.RepositoryViewSet)
