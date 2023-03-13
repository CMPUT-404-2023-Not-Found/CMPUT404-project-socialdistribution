# 2023-03-04
# utils/pagination.py

from collections import OrderedDict
from django.conf import settings
from rest_framework.response import Response
from urllib.parse import urlsplit

from author.models import Author
from post.models import Post
from post.serializers import PostSerializer
from utils.node_comm import NodeComm
from utils.pagination import CustomPagination

NodeComm = NodeComm()

import logging
logger = logging.getLogger('django')
rev = 'rev: $x7toiv$x'

class CommentPagination(CustomPagination):
    lookup_url_kwarg = 'post_uuid'

    def get_paginated_response(self, data):
        post_uuid = self.request.kwargs.get(self.lookup_url_kwarg)
        post_obj = Post.objects.get(id=post_uuid)
        post_id = PostSerializer(post_obj).data['id']
        id = post_id + '/comments'
        
        return Response(OrderedDict([
            ('type', 'comments'),
            ('page', self.page.number),
            ('size', self.page.paginator.per_page),
            ('post', post_id),
            ('id', id),
            ('comments', data)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
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
