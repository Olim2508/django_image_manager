from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import generics, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

from main.models import ImageModel
from main.serializers import (BaseImageSerializer, CreateImageSerializer,
                              ImageOnlySerializer)


def home(request):
    return HttpResponse("Home page")


class ImageViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ImageModel.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "create":
            return CreateImageSerializer
        elif self.action == "get_images_only":
            return ImageOnlySerializer
        return BaseImageSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_images_only(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
