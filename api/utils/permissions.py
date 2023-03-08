# 2023-02-25
# utils/permissions.py

from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsAuthenticatedWithJWT(BasePermission):
    '''
    The request is authenticated with Authorization: Bearer JWT
    '''
    def has_permission(self, request, view):
        is_httpbearer = True if 'Bearer' in request.META.get('HTTP_AUTHORIZATION', '') else False
        return bool(request.user and request.user.is_authenticated and is_httpbearer)

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

class NodeReadOnly(BasePermission):
    '''
    The request is a node and they are doing a read-only request.
    '''

    def has_permission(self, request, view):
        is_in_node_group = request.user.groups.filter(name='node').exists()
        is_httpbasic = True if 'Basic' in request.META.get('HTTP_AUTHORIZATION', '') else False
        is_readonly = bool(request.method in SAFE_METHODS)
        return (is_in_node_group and is_httpbasic and is_readonly)
