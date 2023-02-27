# 2023-02-21
# utils/pagination.py

from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 100
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('items', data)
        ]))
