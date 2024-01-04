from re import S
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

Staff = get_user_model()


class StaffRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Staff
        fields = ("username", "email", "role", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(StaffRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control"}
        )


class StaffChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop("user", None)
        if self.instance == self.user:
            del self.fields["password"]

    class Meta(UserChangeForm.Meta):
        model = Staff
        fields = (
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
            "photo",
        )
