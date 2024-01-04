from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import viewsets, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.response import Response

from staffs.serializers import (
    StaffSerializer,
    ChangePasswordSerializer,
)
from .serializers import MyTokenObtainPairSerializer
from .permissions import IsAdminOrOwner, IsSuperuser

Staff = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class StaffViewset(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (IsAdminOrOwner,)
    # http_method_names = ["get", "head", "put", "patch"]

    @action(detail=False, methods=["post", "get"])
    def reset_password(self, request):
        return redirect("password_reset:reset-password-request")

    @action(detail=True, methods=["post", "get"])
    def change_password(self, request, pk):
        print(pk)
        user = Staff.objects.get(pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            if not user.check_password(old_password):
                return Response(
                    {"errors": {"old_password": "Incorrect old password."}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(new_password)
            user.save()
            return Response(
                {"success": "Password changed successfully."}, status=status.HTTP_200_OK
            )

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
