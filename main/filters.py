from django_filters import rest_framework as filters

from .models import ImageModel, Person


class ImageFilter(filters.FilterSet):
    geo_location = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    created = filters.DateFromToRangeFilter()
    person = filters.CharFilter(method="person_filter")

    def person_filter(self, queryset, name, value):
        return queryset.filter(person__name__icontains=value)

    class Meta:
        model = ImageModel
        fields = ["geo_location", "description", "person"]


class PersonFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Person
        fields = ["name"]
