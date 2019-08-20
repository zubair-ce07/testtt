from rest_framework import generics

from ..models import Requests
from .serializers import RequestSerializer


class RequestApi(generics.ListCreateAPIView):
    """Rest api for users"""

    queryset = Requests.objects.all()
    serializer_class = RequestSerializer
