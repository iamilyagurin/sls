from rest_framework import permissions
from rest_framework.request import Request


def is_safe(request: Request):
    return request.method in permissions.SAFE_METHODS


class ReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return is_safe(request)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if is_safe(request):
            return True

        # Instance must have an attribute named `owner`.
        return request.user and obj.owner_id == request.user.id
