from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'main'

router = DefaultRouter()
router.register(r'photos', views.ImageViewSet)


urlpatterns = [
    path("", views.home, name="home"),
]

urlpatterns += router.urls