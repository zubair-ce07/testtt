from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict


from ..models import Gig, Category, SearchTag, Gallery, \
    Package, Requirements, Faq
from dashboard.models import Offers, Requests
from django.shortcuts import get_object_or_404

from .serializers import GigSerializer, GallerySerializer, \
    PackageSerializer, OfferSerializer
from .permissions import isAdminOrSellerOnly, isSameSeller


class GigApi(generics.ListCreateAPIView):
    """Rest api for seller's gigs"""

    queryset = Gig.objects.all()
    serializer_class = GigSerializer
    permission_classes = (IsAuthenticated, isAdminOrSellerOnly, )

    def create(self, request, *args, **kwargs):
        # FIXME: use serializer instead to using models
        categories = request.data.pop('categories', [])
        search_tags = request.data.pop('search_tags', [])
        faqs = request.data.pop('faqs', [])
        requirements = request.data.pop('requirements', [])
        gig_package = request.data.pop('package', None)
        if not gig_package:
            return Response(
                {'error': "missing attribute 'package'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        gig = Gig.objects.create(
            seller=request.user, **request.data
        )
        # creating package for gig
        package = Package.objects.create(gig=gig, **gig_package)

        for requirement in requirements:
            Requirements.objects.create(gig=gig, **requirement)

        for faq in faqs:
            Faq.objects.create(gig=gig, **faq)

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
    permission_classes = (IsAuthenticated, isAdminOrSellerOnly, isSameSeller, )


class OffersApi(generics.ListCreateAPIView):
    """Rest api for offers
    Seller sends offer to a buyer request
    """

    queryset = Offers.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (IsAuthenticated, isAdminOrSellerOnly, )

    def create(self, request, *args, **kwargs):
        buyer_request_id = request.data.pop('buyer_request_id')
        buyer_request = get_object_or_404(Requests, id=buyer_request_id)
        # setting the required json for serializer
        offer = {
            "seller": request.user.id,
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


class OfferDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for single offer"""

    queryset = Offers.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (IsAuthenticated, )
