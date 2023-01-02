import base64
import imghdr
import uuid
from typing import List

from django.core.files.base import ContentFile
from drf_yasg import openapi
from gprof2dot import basestring
from rest_framework import serializers
from urllib3.packages import six

from main import models

from .models import ImageModel
from .services import ImageService


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if "data:" in data and ";base64," in data:
                header, data = data.split(";base64,")

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (
                file_name,
                file_extension,
            )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension

    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_STRING,
            "title": "Base64Image",
            "description": "Base64 Image",
            "readOnly": False,
        }


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ["name"]


class BaseImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True, required=True, allow_empty_file=False)
    people_in_image = PersonSerializer(many=True, source="person_set")

    class Meta:
        model = models.ImageModel
        fields = ["id", "geo_location", "description", "image", "created_at", "people_in_image"]


class CreateImageSerializer(serializers.Serializer):
    people_in_image = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    image = Base64ImageField(use_url=True, required=True, allow_empty_file=False)
    geo_location = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    def create(self, validated_data):
        if validated_data.get("people_in_image"):
            people_in_image = validated_data.pop("people_in_image")
            image_instance = ImageModel.objects.create(**validated_data)
            ImageService.add_bulk_people_to_image(people_in_image, image_instance)
            return image_instance
        image_instance = ImageModel.objects.create(**validated_data)
        return image_instance


class ImageOnlySerializer(serializers.Serializer):
    image = Base64ImageField(use_url=True, required=True, allow_empty_file=False)
