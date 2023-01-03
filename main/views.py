from django.http import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from main.filters import ImageFilter
from main.models import ImageModel
from main.serializers import (
    BaseImageSerializer,
    CreateImageSerializer,
    ImageOnlySerializer,
)


def home(request):
    return HttpResponse("Home page")


class ImageViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ImageModel.objects.all().order_by("id")
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ImageFilter
    permission_classes_by_action = {
        'create': (IsAuthenticated, ),
        'list': (AllowAny, ),
        'retrieve': (AllowAny, ),
        'get_images_only': (AllowAny, ),
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateImageSerializer
        elif self.action == "get_images_only":
            return ImageOnlySerializer
        return BaseImageSerializer

    def get_images_only(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)
