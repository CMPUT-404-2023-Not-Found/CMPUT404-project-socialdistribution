# 2023-03-15
# comment/pagination.py

from collections import OrderedDict
from django.conf import settings
from rest_framework.response import Response
from urllib.parse import urlsplit

from utils.pagination import CustomPagination

import logging
logger = logging.getLogger('django')
rev = 'rev: $x7toiv$x'

class LikePagination(CustomPagination):
    lookup_url_kwarg = 'post_uuid'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('type', 'liked'),
            ('items', data)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                    'type': {
                        'type': 'string',
                        'example': 'liked'
                    },
                    'items': schema,
              },
          }
