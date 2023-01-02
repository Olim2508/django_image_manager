from django.contrib import admin

from main.models import ImageModel, Person


class PersonInline(admin.StackedInline):
    model = Person
    fields = ("name",)
    fk_name = "image"


@admin.register(ImageModel)
class ImageAdmin(admin.ModelAdmin):
    inlines = [PersonInline]
    list_display = ["id", "description", "geo_location"]
    list_filter = ["description"]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
