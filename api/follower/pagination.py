# 2023-03-15
# Path: follower/pagination.py

from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response

from utils.node_comm import NodeComm
from utils.pagination import CustomPagination

NodeComm = NodeComm()

class FollowerPagination(CustomPagination):
    
    def get_paginated_response(self, data):
        
        return Response(OrderedDict([
            ('items', data)
        ]))

    def get_paginated_response_schema(self, schema):
        
        return {
            'type': 'object',
            'properties': {
                  'items': schema,
              },
          }