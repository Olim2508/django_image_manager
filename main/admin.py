from django.contrib import admin

from main.models import ImageModel


@admin.register(ImageModel)
class ImageAdmin(admin.ModelAdmin):
    pass
