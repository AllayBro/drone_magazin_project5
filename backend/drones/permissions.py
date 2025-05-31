from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только админам редактировать,
    а всем остальным - только читать.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать только владельцу объекта или админу.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
            
        # Проверяем, есть ли у объекта атрибут 'owner'
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
            
        # Для моделей, где владелец называется 'user'
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        return False