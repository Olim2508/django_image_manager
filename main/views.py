from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets

from main.models import ImageModel
from main.serializers import ImageModelSerializer


def home(request):
    return HttpResponse("Home page")

class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageModelSerializer
    queryset = ImageModel.objects.all()

