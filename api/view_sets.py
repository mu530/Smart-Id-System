from cgitb import lookup
from urllib import request
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date

from api.permissions import IsSuperuserOrReadonly, IsSuperuser, IsSuperuserOrCafeStaff
from students.models import Student, EmergencyContact, Device, DisciplinaryRecord
from students.serializers import (
    StudentSerializer,
    EmergencyContactSerializer,
    DeviceSerializer,
    DisciplinaryRecordSerializer,
)
from campuses.models import Department, Campus
from campuses.serializers import DepartmentSerializer, CampusSerializer
from addresses.models import Address
from addresses.serializers import AddressSerializer
from cafe.models import MealPeriod, Attendance
from cafe.serializers import MealSerializer, AttendanceSerializer


class StudentViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsSuperuserOrReadonly,)
    lookup_field = "student_id"


class EmergencyContactViewset(viewsets.ModelViewSet):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = (IsSuperuserOrReadonly,)
    filter_fields = ["student__name", "student__id", "student__student_id"]
    search_fields = ["student__name", "student__student_id"]


class DeviceViewset(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsSuperuserOrReadonly,)
    filter_fields = ["student__name", "student__id", "student__student_id"]
    search_fields = ["student__name", "student__student_id"]


class DisciplinaryRecordViewset(viewsets.ModelViewSet):
    queryset = DisciplinaryRecord.objects.all()
    serializer_class = DisciplinaryRecordSerializer
    filter_fields = ["student__name", "student__id", "student__student_id"]
    search_fields = ["student__name", "student__student_id"]

    def perform_create(self, serializer):
        serializer.save(staff=self.request.user)


# Cumpuses
class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = (IsSuperuserOrReadonly,)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsSuperuserOrReadonly,)


# Addresses
class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [
        IsSuperuserOrReadonly,
    ]


# Cafe
class MealViewset(viewsets.ModelViewSet):
    queryset = MealPeriod.objects.all()
    serializer_class = MealSerializer
    permission_classes = [
        IsSuperuserOrCafeStaff,
    ]


class AttendanceViewset(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [
        IsSuperuserOrCafeStaff,
    ]

    def get_queryset(self):
        Attendance.create_attendance_for_today()  # Run the method to create Attendance objects
        queryset = Attendance.objects.all()

        student_id = self.request.query_params.get("student")
        meal_id = self.request.query_params.get("meal_period")

        if student_id and meal_id:
            queryset = queryset.filter(
                student__student_id=student_id, meal_period_id=meal_id
            )

        queryset = queryset.filter(date_checked=date.today())

        return queryset

    @action(detail=False, methods=["post"])
    def mark_as_eaten(self, request):
        meal_period_id = request.data.get("meal_period")
        student_id = request.data.get("student")

        try:
            attendance = Attendance.objects.get(
                meal_period_id=meal_period_id, student_id=student_id
            )
        except Attendance.DoesNotExist:
            return Response({"message": "Attendance not found."}, status=404)

        if attendance.has_eaten:
            return Response(
                {"message": f"{attendance.student.full_name()} has already eaten."}
            )
        else:
            attendance.has_eaten = True
            attendance.save()
            return Response(
                {
                    "message": f"{attendance.student.full_name()} has been marked as eaten."
                }
            )
