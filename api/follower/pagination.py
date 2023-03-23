# 2023-03-15
# follower/pagination.py

from rest_framework.response import Response
from collections import OrderedDict

from utils.pagination import CustomPagination
from utils.node_comm import NodeComm

NodeComm = NodeComm()

import logging
logger = logging.getLogger('django')
rev = 'rev: $xFgLu67$x'
class FollowerPagination(CustomPagination):

    def get_paginated_response(self, follower_list):
        logger.info(follower_list)
        lookup_list = []
        for follower in follower_list:
            lookup_list.append({
                'type': 'author',
                'object': follower['follower_node_id']
            })
        lookup_results = NodeComm.get_objects(lookup_list)
        
        return Response(OrderedDict([
            ('type', 'followers'),
            ('items', lookup_results)
        ]))
