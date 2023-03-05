# 2023-03-04
# utils/pagination.py

from collections import OrderedDict
from rest_framework.response import Response

from author.models import Author
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

        return Response(OrderedDict([
            ('type', 'inbox'),
            ('author', author_node_id),
            ('items', data)
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
