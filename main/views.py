from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import generics, mixins, status, viewsets
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

    def get_serializer_class(self):
        if self.action == "create":
            return CreateImageSerializer
        if self.action == "list":
            return ImageOnlySerializer
        return BaseImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
