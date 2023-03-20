# 2023-02-13
# node/views.py

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from threading import Thread

from .models import Node
from .serializers import NodeRetrieveSerializer
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

        inbox_urls = request.GET.getlist('url', '')
        if not inbox_urls or len(inbox_urls) == 0:
            logger.error('Missing url query params')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        num_receiving_inbox = len(inbox_urls)
        if num_receiving_inbox > 8:
            logger.error('Too many receiving inboxes [%s], denying request', num_receiving_inbox)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        data_to_send = NodeComm.create_inbox_obj_data(author=request.user, request_data=request.data)
        logger.info('Sending object [%s] [%s] to [%s] inboxes', data_to_send['type'], data_to_send['object'], num_receiving_inbox)
        # This code is modified from a tutorial on Python threads from Lu Zou, on 2019-01-16, retrieved 2023-03-19 from medium.com
        # tutorial here
        # https://medium.com/python-experiments/parallelising-in-python-mutithreading-and-mutiprocessing-with-practical-templates-c81d593c1c49
        thread_list = []
        for inbox_url in inbox_urls:
            thread = Thread(target=NodeComm.send_object, args=(inbox_url, data_to_send))
            thread_list.append(thread)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        return Response(status=status.HTTP_201_CREATED, data=data_to_send)
