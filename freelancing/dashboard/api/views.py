from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from ..models import Requests, RequestFiles
from .serializers import RequestSerializer, RequestFilesSerializer


class RequestApi(generics.ListCreateAPIView):
    """Rest api for users"""

    queryset = Requests.objects.all()
    serializer_class = RequestSerializer


class RequestFilesApi(generics.ListCreateAPIView):
    """Rest api for users"""

    queryset = RequestFiles.objects.all()
    serializer_class = RequestFilesSerializer
    parser_classes = (MultiPartParser, FormParser,)
