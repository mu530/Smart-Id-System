from rest_framework import serializers

from campuses.serializers import DepartmentSerializer
from .models import EmergencyContact, Student, Device, DisciplinaryRecord
from addresses.serializers import AddressSerializer


class EmergencyContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = EmergencyContact
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    emergency = EmergencyContactSerializer()
    devices = DeviceSerializer(many=True)
    department = DepartmentSerializer()

    class Meta:
        model = Student
        fields = "__all__"


class StudentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class DisciplinaryRecordSerializer(serializers.ModelSerializer):
    staff = serializers.CharField(required=False)

    class Meta:
        model = DisciplinaryRecord
        fields = "__all__"
