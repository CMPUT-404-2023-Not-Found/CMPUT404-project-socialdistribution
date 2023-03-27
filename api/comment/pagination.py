# 2023-03-15
# comment/pagination.py

from collections import OrderedDict
from django.conf import settings
from rest_framework.response import Response
from urllib.parse import urlsplit

from author.models import Author
from post.models import Post
from post.serializers import PostSerializer
from utils.pagination import CustomPagination
from utils.node_comm import NodeComm
NodeComm = NodeComm()

import logging
logger = logging.getLogger('django')
rev = 'rev: $x7toiv$x'

class CommentPagination(CustomPagination):
    lookup_url_kwarg = 'post_uuid'

    def get_paginated_response(self, data):
        comment_id = self.request.get_full_path()
        # removes 'comments/' from teh string
        post_id = comment_id[:-9]
        
        lookup_list = []
        for comment in data:
            lookup_list.append({
                **comment,
                'author': comment['author']
            })
        lookup_results = NodeComm.get_objects(lookup_list)
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('type', 'comments'),
            ('page', self.page.number),
            ('size', self.page.paginator.per_page),
            ('post', post_id),
            ('id', comment_id),
            ('comments', lookup_results)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                    'count': {
                        'type': 'integer',
                        'example': 10
                    },
                    'type': {
                        'type': 'string',
                        'example': 'comments'
                    },
                    'page': {
                        'type': 'integer',
                        'example': 1,
                    },
                    'size': {
                        'type': 'integer',
                        'example': 5
                    },
                    'post': {
                        'type': 'string',
                        'format': 'uri',
                        'example': 'http://api.example.com/api/authors/12345678-90ab-cdef-ghij-klmnopqrstuv/posts/12345608-90ac-cd3f-ghxj-klmnooorstuv'
                    },
                    'id': {
                        'type': 'string',
                        'format': 'uri',
                        'example': 'http://api.example.com/api/authors/12345678-90ab-cdef-ghij-klmnopqrstuv/posts/12345608-90ac-cd3f-ghxj-klmnooorstuv/comments'
                    },
                    'comments': schema,
              },
          }
