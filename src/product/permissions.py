from rest_framework import permissions
from user.models import User


class IsSeller(permissions.BasePermission):
    message = "Only seller can add bullion details"

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return False
            return request.user.is_seller
        else:
            return False

    def has_object_permission(self, request, view, obj):
        print('called')
        print(obj, request.user)
        if request.method in permissions.SAFE_METHODS:
            return False
        return request.user.is_seller


class IsVerified(permissions.BasePermission):
    message = " Only Verified User can Perform this action "

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return False
        return request.user.is_verified

    def has_object_permission(self, request, *args, **kwargs):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_verified
        return False


# class IsCompanyVerified(permissions.BasePermission):
#     message = "Your company details are not verified."

#     def has_object_permission(self,request,view,obj):
#         if request.method not in permissions.SAFE_METHODS:
#             return False
#         return request.
