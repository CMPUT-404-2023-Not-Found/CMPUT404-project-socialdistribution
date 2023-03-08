# 2023-02-13
# node/views.py

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import logging

from .models import Node
from .serializers import NodeSerializer
from utils.permissions import IsAuthenticatedWithJWT

logger = logging.getLogger('django')
rev = 'rev: $xCuIts1$x'

class NodeView(GenericAPIView):
    '''
    Node view for node-to-node communication
    '''
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    permission_classes = [IsAuthenticatedWithJWT]

    def post(self, request, *args, **kwargs):
        logger.info(rev)
        serializer = NodeSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error('Request data is bad [%s]', serializer.error_messages)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        request_data = serializer.validated_data
        # Get url from request
        # Figure out credentials from url
        # if cant determine credentials try call anyways but with no creds
        # send http request to url with credentials
        # if response is json return json_parse(response) else return response
        # json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data=request_data)
