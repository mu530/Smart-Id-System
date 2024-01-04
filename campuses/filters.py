import django_filters
from django.db.models import Q

from .models import Campus, Department


class CampusFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_keyword", label="search")

    class Meta:
        model = Campus
        fields = ("search",)

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(name_am__icontains=value))


class DepartmentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_keyword", label="search")

    class Meta:
        model = Department
        fields = ("campus",)

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(name_am__icontains=value))
