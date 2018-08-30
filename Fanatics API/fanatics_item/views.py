from fanatics_item.models import FanaticsItem
from fanatics_item.serializers import FanaticsItemSerializer
from rest_framework import generics


class FanaticsItemList(generics.ListCreateAPIView):
    queryset = FanaticsItem.objects.all()
    serializer_class = FanaticsItemSerializer


class FanaticsItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FanaticsItem.objects.all()
    serializer_class = FanaticsItemSerializer