from django import forms

from .models import MealPeriod, Attendance


class MealForm(forms.ModelForm):
    class Meta:
        model = MealPeriod
        fields = "__all__"
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "start_day": forms.DateInput(attrs={"type": "date"}),
            "end_day": forms.DateInput(attrs={"type": "date"}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ("student", "meal_period")
        widgets = {
            "student": forms.HiddenInput(),
            "meal_period": forms.HiddenInput(),
        }
