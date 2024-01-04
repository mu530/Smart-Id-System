from django.urls import path
from .views import (
    index,
    staff_list_view,
    staff_detail_view,
    staff_login,
    staff_logout,
    staff_register,
    staff_update,
    about,
    ChangePasswordView,
    ResetPasswordView,
    ResetPasswordDoneView,
    ResetPasswordConfirmView,
    ResetPasswordCompleteView,
)

app_name = "Staff"
urlpatterns = [
    path("", index, name="home"),
    path("about/", about, name="about"),
    path("staffs/", staff_list_view, name="staff_list"),
    path("staffs/<int:user_id>/", staff_detail_view, name="staff_detail"),
    path("staffs/<int:user_id>/update", staff_update, name="staff_update"),
    path("<int:user_id>/password/", ChangePasswordView.as_view(), name="password"),
    path("staffs/register/", staff_register, name="register"),
    path("login/", staff_login, name="login"),
    path("logout/", staff_logout, name="logout"),
    path("password_reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password_reset_done/",
        ResetPasswordDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        ResetPasswordConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        ResetPasswordCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
