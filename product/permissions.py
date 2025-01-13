from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Admins have full access (create, update, delete).
    - Users have read-only access (list, retrieve).
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin':  # Admin has full access
                return True
            elif request.user.role == 'user':  # Users have read-only access
                return request.method in ('GET', 'HEAD', 'OPTIONS')
        return False
