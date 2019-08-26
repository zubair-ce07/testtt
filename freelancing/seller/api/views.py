from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


from ..models import Gig, Category, SearchTag, Gallery, \
    Package, Requirements, Faq
from dashboard.models import Requests, Offers

from .serializers import GigSerializer, GallerySerializer, \
    PackageSerializer, RequirementsSerializer, \
    FaqSerializer, OfferSerializer
from .permissions import isAdminOrSellerOnly, isSameSeller, isSameSellerGig
from freelancing.utils.api.response import \
    invalid_serializer_response, missing_attribute_response


class GigApi(generics.ListCreateAPIView):
    """Rest api for seller's gigs"""

    queryset = Gig.objects.all()
    serializer_class = GigSerializer
    permission_classes = (IsAuthenticated, isAdminOrSellerOnly, )

    def create(self, request, *args, **kwargs):
        categories = request.data.pop('categories', [])
        search_tags = request.data.pop('search_tags', [])
        faqs = request.data.pop('faqs', [])
        requirements = request.data.pop('requirements', [])
        gig_package = request.data.pop('package', None)

        if not gig_package:
            return missing_attribute_response('package')
        if not categories:
            return missing_attribute_response('categories')
        if not search_tags:
            return missing_attribute_response('search_tags')

        gig_serializer = GigSerializer(
            data={"seller": request.user.id, **request.data}
        )
        if not gig_serializer.is_valid():
            return invalid_serializer_response(gig_serializer)

        gig = gig_serializer.save()

        pkg_serializer = PackageSerializer(
            data={"gig": gig.id, **gig_package}
        )
        if not pkg_serializer.is_valid():
            return invalid_serializer_response(pkg_serializer)

        pkg_serializer.save()

        for requirement in requirements:
            req_serializer = RequirementsSerializer(
                data={"gig": gig.id, **requirement}
            )
            if not req_serializer.is_valid():
                return invalid_serializer_response(req_serializer)
            req_serializer.save()

        for faq in faqs:
            faq_serializer = FaqSerializer(
                data={"gig": gig.id, **faq}
            )
            if not faq_serializer.is_valid():
                return invalid_serializer_response(faq_serializer)
            faq_serializer.save()

        for category in categories:
            category = Category.objects.get(id=category["id"])
            gig.categories.add(category)

        for search_tag in search_tags:
            search_tag = SearchTag.objects.get(id=search_tag["id"])
            gig.search_tags.add(search_tag)

        queryset = self.get_queryset()
        serializer = GigSerializer(queryset, many=True)

        # saving data
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GigDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for seller's gig details"""

    queryset = Gig.objects.all()
    serializer_class = GigSerializer
    permission_classes = (IsAuthenticated, isAdminOrSellerOnly, isSameSeller, )


class GalleryFilesApi(generics.ListCreateAPIView):
    """Rest api for seller gig's gallery files"""

    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (IsAuthenticated, isAdminOrSellerOnly, )
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        gig_id = request.data.get("gig_id")
        if not gig_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        gig = Gig.objects.get(id=gig_id)
        gallery_files = []
        for uploaded_file in request.data.getlist('files'):
            gallery_file = Gallery.objects.create(
                gig=gig,
                gig_image=uploaded_file
            )
            gallery_file.save()
            gallery_files.append(gallery_file)

        serializer = GallerySerializer(gallery_files, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GalleryFilesDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for seller gig's gallery files details"""

    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (
        IsAuthenticated,
        isAdminOrSellerOnly,
        isSameSellerGig,
    )


class OffersApi(generics.ListCreateAPIView):
    """Rest api for offers
    Seller sends offer to a buyer request by specifying his gig
    """

    queryset = Offers.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (
        IsAuthenticated,
        isAdminOrSellerOnly,
        isSameSellerGig,
    )

    def create(self, request, *args, **kwargs):
        buyer_request_id = request.data.pop('buyer_request_id')
        buyer_request = get_object_or_404(Requests, id=buyer_request_id)
        gig_id = request.data.pop('gig_id')
        gig = get_object_or_404(Gig, id=gig_id)
        # setting the required json for serializer
        offer = {
            "gig": gig.id,
            "buyer_request": buyer_request.id,
            **request.data
        }

        serializer = OfferSerializer(data=offer)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # saving data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
