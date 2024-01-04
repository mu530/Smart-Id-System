from dataclasses import field
import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

Staff = get_user_model()


class StaffFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_keyword", label="search")

    class Meta:
        model = Staff
        fields = ("role",)
        exclude = ("photo",)

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value)
            | Q(email__icontains=value)
            | Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
        )
