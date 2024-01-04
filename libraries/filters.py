import django_filters
from django.db.models import Q

from .models import Library


class BorrowerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_keyword", label="search")

    class Meta:
        model = Library
        fields = ("search",)

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(student__first_name__icontains=value)
            | Q(student__last_name__icontains=value)
            | Q(student__student_id__icontains=value)
        )


class BookFilter(django_filters.FilterSet):
    search_book = django_filters.CharFilter(method="filter_by_keyword", label="search")

    class Meta:
        model = Library
        fields = ("search_book",)

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(Q(author__icontains=value) | Q(title__icontains=value))
