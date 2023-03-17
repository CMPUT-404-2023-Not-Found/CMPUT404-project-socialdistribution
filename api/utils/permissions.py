# 2023-02-25
# utils/permissions.py

from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
WRITE_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')

import logging
logger = logging.getLogger('django')
rev = 'rev: $xNEina1$x'

class IsAuthenticatedWithJWT(BasePermission):
    '''
    The request is authenticated with Authorization: Bearer JWT
    and method is SAFE
    '''
    def has_permission(self, request, view):
        is_readonly = bool(request.method in SAFE_METHODS)
        is_httpbearer = True if 'Bearer' in request.META.get('HTTP_AUTHORIZATION', '') else False
        return bool(request.user and request.user.is_authenticated and is_httpbearer and is_readonly)

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

class OwnerCanWrite(BasePermission):
    '''
    The request is the owner of the requested resource and they are doing
    a write operation. 
    '''
    def has_permission(self, request, view):
        author_uuid = view.kwargs.get('author_uuid') if view.kwargs.get('author_uuid') else view.kwargs.get('id')
        is_writeop = bool(request.method in WRITE_METHODS)
        is_owner = True if str(request.user.id) == str(author_uuid) else False
        return (is_writeop and is_owner)

class NodeReadOnly(BasePermission):
    '''
    The request is a node and they are doing a read-only request.
    '''

    def has_permission(self, request, view):
        is_in_node_group = request.user.groups.filter(name='node').exists()
        is_httpbasic = True if 'Basic' in request.META.get('HTTP_AUTHORIZATION', '') else False
        is_readonly = bool(request.method in SAFE_METHODS)
        return (is_in_node_group and is_httpbasic and is_readonly)
