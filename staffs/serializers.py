from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

Staff = get_user_model()


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        exclude = ("user_permissions",)
        read_only_fields = ("date_joined", "last_login")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        group_ids = validated_data.pop("groups")
        password = validated_data.pop("password")
        print(validated_data)
        user = Staff(**validated_data)
        user.set_password(password)
        user.save()
        groups = Group.objects.filter(id__in=group_ids)
        user.groups.set(groups)
        return user

    def update(self, instance, validated_data):
        validated_data.pop("password", None)
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Staff
        fields = ("old_password", "new_password", "confirm_new_password")

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs
