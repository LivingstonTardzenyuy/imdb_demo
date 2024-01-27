from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        else:
            return bool(request.user and request.user.is_staff)

class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        #we use has_object_permission since we are dealing with objects. 
        if request.method in permissions.SAFE_METHODS:
            # read-only request
            return True 
        else:
            return obj.review_user == request.user 



