from rest_framework.permissions import SAFE_METHODS, BasePermission


class OrderDeletePermission(BasePermission):
    def has_object_permission(self, request, view, vacation_obj):
        if request.method not in SAFE_METHODS:
            return request.user.id == vacation_obj.user.id