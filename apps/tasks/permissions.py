from rest_framework.permissions import BasePermission

class IsManagerOrDeveloper(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_manager() or request.user.is_developer())
