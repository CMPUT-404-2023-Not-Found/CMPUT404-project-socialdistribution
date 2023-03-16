# 2023-03-15
# follower/pagination.py

from rest_framework.response import Response
from collections import OrderedDict

from utils.pagination import CustomPagination

class FollowerPagination(CustomPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('type', 'followers'),
            ('items', data)
        ]))

