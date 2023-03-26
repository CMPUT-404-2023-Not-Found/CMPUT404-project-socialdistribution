# 2023-02-13
# node/views.py

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from threading import Thread

from .models import Node
from .serializers import NodeRetrieveSerializer, NodeListSerializer
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
    serializer_class = NodeRetrieveSerializer
    permission_classes = [IsAuthenticated]

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
        object_data = {
            'type': object_type,
            'object': object_url
        }
        lookup_results = NodeComm.get_objects([object_data])
        if lookup_results:
            return Response(status=status.HTTP_200_OK, data=lookup_results)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        '''
        Post an object to a node's author's inboxes
        '''
        logger.info(rev)
        inbox_urls = request.data.get('inbox_urls', [])
        num_receiving_inbox = len(inbox_urls)
        max_receiving_inbox = 32
        if not num_receiving_inbox or num_receiving_inbox > max_receiving_inbox:
            logger.error('Invalid number of inboxes [%s] supported [%s], denying request', num_receiving_inbox, max_receiving_inbox)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        data_to_send = NodeComm.create_inbox_obj_data(author=request.user, request_data=request.data)
        logger.info('Sending object [%s] [%s] to [%s] inboxes', data_to_send['type'], data_to_send['object'], num_receiving_inbox)
        thread = Thread(target=NodeComm.send_object, args=(inbox_urls, data_to_send))
        thread.start()
        return Response(status=status.HTTP_201_CREATED, data=data_to_send)

class NodeListView(ListAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeListSerializer
    permission_classes = [IsAuthenticated]