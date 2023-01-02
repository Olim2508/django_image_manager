from django.http import HttpResponse
from django.shortcuts import redirect, render
from django_filters import rest_framework as filters
from rest_framework import generics, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

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

    def get_serializer_class(self):
        if self.action == "create":
            return CreateImageSerializer
        elif self.action == "get_images_only":
            return ImageOnlySerializer
        return BaseImageSerializer

    def get_images_only(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)
