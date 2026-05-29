from rest_framework.permissions import BasePermission

class IsUserOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return request.user == obj.user
        except AttributeError:
            return request.user == obj.owner