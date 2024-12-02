from rest_framework import permissions

class ManagerUser(permissions.BasePermission):
    message =  'You are not authorized'

    def has_permission(self, request, view):
        role = request.user.groups.filter(name = 'Manager').exists()
        if role or request.user.is_superuser:
            return True
        return False