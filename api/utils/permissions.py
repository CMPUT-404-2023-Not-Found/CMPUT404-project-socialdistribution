# 2023-02-25
# utils/permissions.py

from rest_framework.permissions import BasePermission

class AnonymousCanPost(BasePermission):
    '''
    The request is anonymous as a user, but only allowed for POST methods.
    Useful when used in conjunction with IsAdmin to allow anonymous users
    to create things but only admins can retrieve lists of said things.
    '''
    def has_permission(self, request, view):
        if (request.method == 'POST' and 
            request.user and request.user.is_anonymous): 
            return True
        return False
