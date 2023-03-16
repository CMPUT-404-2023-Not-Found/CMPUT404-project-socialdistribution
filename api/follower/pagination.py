# 2023-03-15
# follower/pagination.py

from rest_framework.response import Response
from collections import OrderedDict

from utils.pagination import CustomPagination
from utils.node_comm import NodeComm
from .models import Author

NodeComm = NodeComm()

import logging
logger = logging.getLogger('django')
rev = 'rev: $xFgLu67$x'
class FollowerPagination(CustomPagination):

    def get_paginated_response(self, data):
        new_data = []
        for item in data:
            item_data = NodeComm.get_object('author', item['follower'])
            if item_data:
                new_data.append(item_data)
            else:
                logger.warning('Failed lookup on item type [%s] url [%s]', 'author', item['follower'])
                new_data.append(item)
        
        return Response(OrderedDict([
            ('type', 'followers'),
            ('items', new_data)
        ]))

