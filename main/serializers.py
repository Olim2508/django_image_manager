import base64
from rest_framework import serializers
from gprof2dot import basestring
from django.core.files.base import ContentFile
from drf_yasg import openapi

from main import models


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, basestring) and data.startswith('data:image'):
            format_, imgstr = data.split(';base64,')
            ext = format_.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
            return None
        return super(Base64ImageField, self).to_internal_value(data)

    def to_representation(self, value):
        if value.name == '' or value.name is None:
            return ''
        try:
            with open(value.path, "rb") as image_file:
                return 'data:image/%s;base64,%s' % (
                    value.name.split('.')[-1],
                    base64.b64encode(image_file.read()).decode("utf-8")
                )
        except (FileNotFoundError,):
            return ''

    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_STRING,
            "title": "Base64Image",
            "description": 'Base64 Image',
            "readOnly": False
        }


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ImageModel
        fields = "__all__"
