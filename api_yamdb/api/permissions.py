from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Только для Автора"""

    def has_object_permission(self, request, view, obj):

        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Если админ, то можно всё, иначе - только чтение"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_admin
                )
            )
        )


class IsAdminOnly(permissions.BasePermission):
    """Только для админа, сотрудника или суперпользователя"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
            )
        return False


class IsAuthorOrModerOrAdminOrReadOnly(permissions.BasePermission):
    """Ограничение для Отзывов и Комментарий:"""
    """1. Оставлять новые и оценивать может только"""
    """аутентифицированный пользователь"""
    """2. Удалять и изменять могут:"""
    """2.1. Аутентифицированный пользователь - только своё"""
    """2.2. Модератор и Админ - вообще всё"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
