from rest_framework import permissions

from accounts.models import UserRole, Role
from accounts.serializer import UserRoleSerializer
from main.models import StayOrder


class AdminPermission(permissions.BasePermission):
    serializer = UserRoleSerializer

    def has_permission(self, request, view):
        try:
            user_role = UserRole.objects.get(user=request.user)
            return user_role.role.name == 'admin'
        except UserRole.DoesNotExist:
            return False

