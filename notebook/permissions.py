from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission that allows only the owner of an object to edit or delete it.
    Others can only read (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are read-only requests (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the owner can modify or delete
        return obj.owner == request.user
