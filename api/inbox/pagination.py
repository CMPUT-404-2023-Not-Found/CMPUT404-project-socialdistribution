# 2023-03-04
# utils/pagination.py

from collections import OrderedDict
from django.conf import settings
from rest_framework.response import Response
from urllib.parse import urlsplit

from author.models import Author
from post.models import Post
from post.serializers import PostSerializer
from utils.pagination import CustomPagination

import logging
logger = logging.getLogger('django')
rev = 'rev: $xFgLu67$x'

class InboxPagination(CustomPagination):
    lookup_url_kwarg = 'author_uuid'

    def get_paginated_response(self, data):
        author_uuid = self.request.kwargs.get(self.lookup_url_kwarg)
        author_obj = Author.objects.get(id=author_uuid)
        author_node_id = author_obj.get_node_id()

        new_data = []
        for item in data:
            item_urlparse = urlsplit(item['object'])
            item_url = item_urlparse.scheme + '://' + item_urlparse.netloc
            if item_url == settings.APP_URL:
                new_data.append(self.get_internal_object_detail(item))
            else:
                new_data.append(self.get_external_object_detail(item))

        return Response(OrderedDict([
            ('type', 'inbox'),
            ('author', author_node_id),
            ('items', new_data)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                    'type': {
                        'type': 'string',
                        'example': 'inbox'
                    },
                    'author': {
                        'type': 'string',
                        'format': 'uri',
                        'example': 'http://api.example.com/api/authors/12345678-90ab-cdef-ghij-klmnopqrstuv'
                    },
                    'items': schema,
              },
          }

    def get_internal_object_detail(self, object):
        '''
        Call internal database for object information
        '''
        ret = object
        if object['type'] == 'post':
            # Get the uuid of the thing for serialization
            object_uuid = object['object'].rstrip('/').split('/')[-1]
            object_data = Post.objects.get(id=object_uuid)
            serializer = PostSerializer(object_data)
            ret = serializer.data
        return ret

    def get_external_object_detail(self, object):
        '''
        Call external nodes for object information 
        '''
        return object
