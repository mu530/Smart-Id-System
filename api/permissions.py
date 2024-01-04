import re
from rest_framework import permissions


class IsAdminOrOwner(permissions.IsAuthenticated, permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return (request.user.is_superuser) or (obj == request.user)


class IsSuperuser(permissions.IsAuthenticated, permissions.BasePermission):
    def has_permission(self, request, view):
        # permissions are only allowed to Super users
        return request.user.is_superuser


class IsSuperuserOrReadonly(permissions.IsAuthenticated, permissions.BasePermission):
    def has_permission(self, request, view):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # permissions are only allowed to Super users
        return request.user.is_superuser


class IsSuperuserOrCafeStaff(permissions.IsAuthenticated, permissions.BasePermission):
    def has_permission(self, request, view):
        # permissions are allowed to Super users
        if request.user.is_superuser or request.user.role == "CAFE_STAFF":
            return True
