# 2023-02-13
# node/views.py

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

from .models import Node
from .serializers import NodeRetrieveSerializer, NodeSendSerializer
from utils.node_comm import NodeComm

NodeComm = NodeComm()

logger = logging.getLogger('django')
rev = 'rev: $xCuIts1$x'

class NodeView(GenericAPIView):
    '''
    Node view for node-to-node communication
    '''
    queryset = Node.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if (self.request.method in ['post', 'put']):
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
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.error('Request data is bad [%s]', serializer.error_messages)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        request_data = serializer.validated_data

        object_url = request_data.get('url')
        object_type = request_data.get('type')
        logger.info('Doing lookup of object_type [%s] object_url [%s]', object_type, object_url)
        object_data = NodeComm.get_object(type=object_type, url=object_url)
        if object_data:
            return Response(status=status.HTTP_200_OK, data=object_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
