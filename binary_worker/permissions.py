from rest_framework.permissions import BasePermission


class GroupAOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Group_A').exists()


class GroupBOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Group_B').exists()
