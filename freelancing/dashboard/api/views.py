from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from ..models import Requests, RequestFiles, Offers
from seller.models import Category
from .serializers import RequestSerializer, RequestFilesSerializer
from .permissions import isAdminOrBuyerOnly, \
    isSameBuyer, isSameBuyerRequest, isSameBuyerOffer
from freelancing.utils.api.response import \
    invalid_serializer_response, missing_attribute_response
from seller.api.serializers import OfferSerializer


class RequestApi(generics.ListCreateAPIView):
    """Rest api for buyer's requests"""

    queryset = Requests.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated, isAdminOrBuyerOnly, )

    def create(self, request, *args, **kwargs):
        categories = request.data.pop('categories', [])
        if not categories:
            return missing_attribute_response('categories')

        request_serializer = RequestSerializer(
            data={"buyer": request.user.id, **request.data}
        )
        if not request_serializer.is_valid():
            return invalid_serializer_response(request_serializer)
        buyer_request = request_serializer.save()

        for category in categories:
            category = Category.objects.get(id=category["id"])
            buyer_request.categories.add(category)

        return Response(
            request_serializer.data,
            status=status.HTTP_201_CREATED
        )


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
    permission_classes = (
        IsAuthenticated, isAdminOrBuyerOnly, isSameBuyerRequest, )


class OfferDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for single offer"""

    queryset = Offers.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (IsAuthenticated, isSameBuyerOffer)
