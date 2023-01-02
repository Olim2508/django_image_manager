from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "main"

router = DefaultRouter()
router.register(r"images", views.ImageViewSet)


urlpatterns = [
    path("", views.home, name="home"),
    path("images/only/", views.ImageViewSet.as_view({"get": "get_images_only"}), name="get_images_only"),
]

urlpatterns += router.urls
