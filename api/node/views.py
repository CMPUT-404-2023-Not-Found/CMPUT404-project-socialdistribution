# 2023-02-13
# node/views.py

import json
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Node
from .serializers import NodeRetrieveSerializer, NodeSendSerializer
from utils.node_comm import NodeComm

NodeComm = NodeComm()

import logging
logger = logging.getLogger('django')
rev = 'rev: $xCuIts1$x'

class NodeView(GenericAPIView):
    '''
    Node view for node-to-node communication
    '''
    queryset = Node.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if (self.request.method == 'POST'):
            return NodeSendSerializer
        else:
            return NodeRetrieveSerializer

    def get(self, request, *args, **kwargs):
        '''
        Get an object from another node
        '''
        logger.info(rev)
        object_url = request.GET.get('url', '')
        object_type = request.GET.get('type', '')
        query_data = {
            'url': object_url,
            'type': object_type
        }
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=query_data)
        if not serializer.is_valid():
            logger.error('Request query data is bad [%s]', serializer.error_messages)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        logger.info('Doing lookup of object_type [%s] object_url [%s]', object_type, object_url)
        object_data = NodeComm.get_object(type=object_type, url=object_url)
        if object_data:
            return Response(status=status.HTTP_200_OK, data=object_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        '''
        Post an object to a node's author's inboxes
        '''
        logger.info(rev)
        req_data = {
            '@context': 'https://www.w3.org/ns/activitystreams',
            'author': request.user.get_node_id(),
            'type': request.data.get('type', ''),
            'object': request.data.get('object', ''),
            'summary': request.data.get('summary', '')
        }
        if not req_data.get('summary'): 
            requester_name = request.user.display_name if request.user.display_name else request.user.username
            req_type = req_data['type']
            req_data.summary = f'{requester_name} sent a {req_type}'

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=req_data)
        if not serializer.is_valid():
            logger.error('Request data is bad [%s]', serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        data_to_send = json.dumps(serializer.data)

        inbox_url = request.GET.get('url', '')
        logger.info('Sending a [%s] object to inbox [%s]', req_data['type'], inbox_url)
        response_data, response_status = NodeComm.send_object(inbox_url=inbox_url, data=data_to_send)
        if response_status == 201:
            return Response(status=status.HTTP_201_CREATED, data=response_data)
        else:
            return Response(status=response_status)
