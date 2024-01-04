import django_filters
from django.db.models import Q

from .models import Student


class StudentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_keyword", label="search")

    class Meta:
        model = Student
        fields = (
            "student_id",
            "gender",
            "government_id_number",
            "department",
            "is_cafe_user",
            "year",
        )

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(first_name_am__icontains=value)
            | Q(last_name_am__icontains=value)
        )
