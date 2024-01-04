from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import StaffViewset, MyTokenObtainPairView
from .view_sets import (
    StudentViewset,
    EmergencyContactViewset,
    DeviceViewset,
    DepartmentViewSet,
    CampusViewSet,
    AddressViewset,
    MealViewset,
    AttendanceViewset,
    DisciplinaryRecordViewset,
)

router = SimpleRouter()
router.register("staffs", StaffViewset, basename="staffs")

# Students
router.register("students", StudentViewset, basename="students")
router.register("emergency", EmergencyContactViewset, basename="emergency")
router.register("device", DeviceViewset, basename="device")
router.register("disciplin", DisciplinaryRecordViewset, basename="disciplin")

# Cumpuses
router.register("campuses", CampusViewSet, basename="campuses")
router.register("departments", DepartmentViewSet, basename="departments")

# Addresses
router.register("address", AddressViewset, basename="address")

# Cafe
router.register("cafe/meal", MealViewset, basename="meal")
router.register("cafe/attendance", AttendanceViewset, basename="meal")


urlpatterns = router.urls

urlpatterns += [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "password/reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
