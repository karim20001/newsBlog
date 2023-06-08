from rest_framework import permissions


#users update-delete own posts only
class AuthenticateOwnerPost(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user