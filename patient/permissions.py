from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if not request.user or request.user.is_anonymous:
            return False
        return request.user.is_patient
