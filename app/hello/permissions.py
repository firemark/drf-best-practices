from rest_framework.permissions import BasePermission


class PagePermission(BasePermission):
    message = 'another user not allowed'

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        user = request.user
        return user.is_admin or user.is_moderator or obj.user == request.user
