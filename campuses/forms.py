from django import forms
from .models import Campus, Department


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        exclude = ("address",)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
