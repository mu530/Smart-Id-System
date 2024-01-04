from rest_framework import serializers

from .models import Campus, Department
from addresses.serializers import AddressSerializer


class CampusSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = Campus
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(many=False)

    class Meta:
        model = Department
        fields = "__all__"
