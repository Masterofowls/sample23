from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение, позволяющее редактировать объект только его автору.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение разрешены для любого запроса
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешения на запись только для автора объекта
        return obj.author == request.user
