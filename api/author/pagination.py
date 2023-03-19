# 2023-03-18
# author/pagination.py

from collections import OrderedDict
from rest_framework.response import Response

from utils.pagination import CustomPagination

import logging
logger = logging.getLogger('django')
rev = 'rev: $xFgLu67$x'

class AuthorPagination(CustomPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('type', 'authors'),
            ('items', data)
        ]))
