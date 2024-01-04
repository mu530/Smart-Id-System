from django.urls import path
from .views import campus_form, campus_list

app_name = "Campus"

urlpatterns = [
    path("register/", campus_form, name="register"),
    path("list/", campus_list, name="list"),
]
