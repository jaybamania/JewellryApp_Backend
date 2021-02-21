from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    message = "You are not Super Admin"

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    message = "You are not Admin"

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_admin
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class IsSuperAdminOrAdmin(permissions.BasePermission):
    message = "You are not Super Admin or Admin"

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_admin or request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_superuser


class IsActive(permissions.BasePermission):
    message = "Contact admin to enable your account"

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_admin
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class UpdateOwnDetail(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class IsVerified(permissions.BasePermission):
    message = "Not verified Verify his Phone number to get Access to all other pages"

    def has_permission(self, request, view):

        if not request.user.is_anonymous:
            if request.user.is_superuser:
                return True
            return request.user.is_verified
        else:
            return False
