from rest_framework import serializers

from students.serializers import StudentShortSerializer
from .models import MealPeriod, Attendance


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPeriod
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentShortSerializer(many=False)

    class Meta:
        model = Attendance
        fields = "__all__"
