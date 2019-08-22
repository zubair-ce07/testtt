from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from ..models import Requests, RequestFiles
from seller.models import Category
from .serializers import RequestSerializer, RequestFilesSerializer
from .permissions import isAdminOrBuyerOnly, isSameBuyer


class RequestApi(generics.ListCreateAPIView):
    """Rest api for buyer's requests"""

    queryset = Requests.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated, isAdminOrBuyerOnly, )

    def create(self, request, *args, **kwargs):
        categories = request.data.pop('categories', [])

        buyer_request = Requests.objects.create(
            buyer=request.user, **request.data
        )
        for category in categories:
            category = Category.objects.get(id=category["id"])
            buyer_request.categories.add(category)

        queryset = self.get_queryset()
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RequestDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for buyer's request details"""

    queryset = Requests.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated, isAdminOrBuyerOnly, isSameBuyer, )


class RequestFilesApi(generics.ListCreateAPIView):
    """Rest api for buyer request's files"""

    queryset = RequestFiles.objects.all()
    serializer_class = RequestFilesSerializer
    permission_classes = (IsAuthenticated, isAdminOrBuyerOnly, )
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        buyer_request_id = request.data.get("buyer_request_id")
        if not buyer_request_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        buyer_request = Requests.objects.get(id=buyer_request_id)
        request_files = []
        for uploaded_file in request.data.getlist('files'):
            request_file = RequestFiles.objects.create(
                request=buyer_request,
                file_name=uploaded_file
            )
            request_file.save()
            request_files.append(request_file)

        serializer = RequestFilesSerializer(request_files, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RequestFilesDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for buyer's request files details"""

    queryset = RequestFiles.objects.all()
    serializer_class = RequestFilesSerializer
    permission_classes = (IsAuthenticated, isAdminOrBuyerOnly, isSameBuyer, )
