from rest_framework import permissions
from django.contrib.auth.models import Group


class IsAssistantUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            is_in_group = Group.objects.get(name='assistant').user_set.filter(id=request.user.id).exists()
        except Group.DoesNotExist:
            print("error")
            # return False

        print("is in group", is_in_group)
        return request.user and is_in_group
