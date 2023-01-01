from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect


from rest_framework import viewsets, status
from rest_framework.response import Response

from main.models import ImageModel
from main.serializers import BaseImageSerializer, CreateUpdateImageSerializer


def home(request):
    return HttpResponse("Home page")


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            print(self.action)
            return CreateUpdateImageSerializer
        return BaseImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

