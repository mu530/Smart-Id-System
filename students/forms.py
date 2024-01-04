from django import forms
from django.forms.widgets import DateTimeInput

from .models import *


Staff = get_user_model()


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        exclude = ("address",)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ("student_id", "qr_code", "address", "emergency")
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": str(
                        datetime.date.today() - datetime.timedelta(days=10 * 365)
                    ),
                }
            ),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ("student", "date_added")


class DisciplinaryRecordForm(forms.ModelForm):
    class Meta:
        model = DisciplinaryRecord
        fields = ("reason",)
