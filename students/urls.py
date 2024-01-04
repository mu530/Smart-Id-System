from django.urls import path
from .views import (
    students_list,
    student_register,
    update_student_profile,
    student_profile,
    add_device,
    add_disciplinary_record,
    id_card,
    update_disciplinary_record,
)

app_name = "Student"

urlpatterns = [
    path("", students_list, name="student_list"),
    path("register/", student_register, name="register"),
    path("id_card/", id_card, kwargs={"id": None}, name="id_card"),
    path("<str:id>/", student_profile, name="profile"),
    path("<str:id>/update/", update_student_profile, name="profile_update"),
    path("<str:id>/device/", add_device, name="new_device"),
    path("<str:id>/disciplin/add/", add_disciplinary_record, name="add_disciplin"),
    path("<str:id>/id_card/", id_card, name="id_card"),
    path("dis/<str:id>/update/", update_disciplinary_record, name="update_dis"),
]
