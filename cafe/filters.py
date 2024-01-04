import django_filters
from django.db.models import Q
from django.forms import TimeInput, DateInput, TextInput

from cafe.models import Attendance, MealPeriod


class TimeRangeField(django_filters.CharFilter):
    def filter(self, queryset, value):
        if value:
            start_time, end_time = value.split("-")
            queryset = queryset.filter(
                start_time__gte=start_time, end_time__lte=end_time
            )
        return queryset


class DateRangeField(django_filters.CharFilter):
    def filter(self, queryset, value):
        if value:
            start_day, end_day = value.split("-")
            queryset = queryset.filter(start_day__gte=start_day, end_day__lte=end_day)
        return queryset


class CafeUserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_by_keyword",
        label="search cafe users",
        widget=TextInput(attrs={"type": "search"}),
    )

    class Meta:
        model = Attendance
        fields = ("search",)

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(student__first_name__icontains=value)
            | Q(student__last_name__icontains=value)
            | Q(student__first_name_am__icontains=value)
            | Q(student__last_name_am__icontains=value)
            | Q(student__student_id__icontains=value)
        )


class MealFilter(django_filters.FilterSet):
    time_range = TimeRangeField(
        field_name="start_time",
        label="Time Range",
        widget=TimeInput(attrs={"type": "time"}),
    )
    date_range = DateRangeField(
        field_name="start_day",
        label="Date Range",
        widget=DateInput(attrs={"type": "date"}),
    )
    search = django_filters.CharFilter(
        method="filter_by_keyword", label="search students"
    )

    class Meta:
        model = MealPeriod
        fields = ("search", "time_range", "date_range")

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(meal_period__icontains=value) | Q(meal_period_am__icontains=value)
        )
