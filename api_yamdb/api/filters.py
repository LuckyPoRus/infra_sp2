from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class FilterTitle(FilterSet):
    category = CharFilter(
        field_name="category__slug",
    )
    genre = CharFilter(
        field_name="genre__slug",
    )
    name = CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )
    rating = CharFilter(
        field_name="rating__slug",
    )

    class Meta:
        model = Title
        fields = ("__all__")
