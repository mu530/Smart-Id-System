from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import StaffRegistrationForm, StaffChangeForm
from django.contrib.auth.forms import UserChangeForm

Staff = get_user_model()


class StaffAdmin(admin.ModelAdmin):
    form = StaffChangeForm
    list_display = ["username", "email", "display_full_name", "role", "is_superuser"]
    list_filter = ("is_staff", "is_superuser", "role")
    search_fields = ("username", "email", "first_name", "last_name")

    def display_full_name(self, obj):
        return obj.get_full_name()

    display_full_name.short_description = "Full Name"


admin.site.register(Staff, StaffAdmin)
