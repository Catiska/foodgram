from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Разрешение на изменение автору, остальным только чтение."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    """Разрешение на изменение только админу, остальным только чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff
