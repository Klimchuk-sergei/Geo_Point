from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Чтение разрешено всем, запись — только автору.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'created_by', getattr(obj, 'user', None))
        return owner == request.request.user