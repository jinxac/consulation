from rest_framework import permissions
from django.contrib.auth.models import Group


class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            is_in_group = Group.objects.get(name='client').user_set.filter(id=request.user.id).exists()
        except Group.DoesNotExist:
            return False

        return request.user and is_in_group
