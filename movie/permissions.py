"""from rest_framework import permissions


class IsWatcher(permissions.BasePermission):
    message = 'user is not watcher'

    def has_permission(self, request, view):
        return request.user.role == 'watcher'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'watcher'


class IsReviewer(permissions.BasePermission):
    message = 'user is not a reviewer'

    def has_permission(self, request, view):
        return request.user.role == 'reviewer'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'reviewer'"""

