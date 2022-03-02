from rest_framework import permissions

class UsersPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'update', 'partial_update']:
            return bool(request.user and request.user.is_authenticated)
        elif view.action in ['create', 'destroy']:
            return bool(request.user and request.user.is_staff and request.user.is_authenticated)
        else:
            return False


class ElectionsPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user)
        if view.action in ['retrieve', 'list']:
            return bool(request.user and request.user.is_authenticated)
        elif view.action in ['create', 'destroy', 'update', 'partial_update']:
            return bool(request.user and request.user.is_staff and request.user.is_authenticated)
        else:
            return False


class GroupsPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return bool(request.user and request.user.is_authenticated)
        elif view.action in ['create', 'destroy', 'update', 'partial_update']:
            return bool(request.user and request.user.is_staff and request.user.is_authenticated)
        else:
            return False