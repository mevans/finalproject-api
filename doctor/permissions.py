from rest_framework import permissions


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        return request.user.is_doctor
