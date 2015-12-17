from rest_framework import routers

from Gitpard.apps.repository import views

router = routers.DefaultRouter()
router.register(r'repositories', views.RepositoryViewSet)
