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
    invalid_serializer_response, missing_attribute_response, does_not_exists_response
from seller.api.serializers import OfferSerializer


class RequestApi(generics.ListCreateAPIView):
    """Rest api for buyer's requests"""

    queryset = Requests.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated, isAdminOrBuyerOnly, )

    def create(self, request, *args, **kwargs):
        request_categories = request.data.pop('categories', [])
        if not request_categories:
            return missing_attribute_response('categories')

        request_serializer = RequestSerializer(
            data={"buyer": request.user.id, **request.data}
        )
        if not request_serializer.is_valid():
            return invalid_serializer_response(request_serializer)

        categories = []
        for category in request_categories:
            category = Category.objects.filter(id=category["id"])
            if not category.exists():
                return does_not_exists_response('category')
            categories.append(category.get())

        buyer_request = request_serializer.save()
        buyer_request.categories.set(categories)

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
            return missing_attribute_response('buyer_request_id')

        buyer_request = Requests.objects.filter(id=buyer_request_id)
        if not buyer_request.exists():
            return does_not_exists_response('Buyer Request')
        buyer_request = buyer_request.get()

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
