from rest_framework import permissions, throttling


class UserPermissions(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return not bool(request.user.is_authenticated)


class PostAnononymousRateThrottle(throttling.AnonRateThrottle):
    scope = 'post_anon'

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)