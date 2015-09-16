from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Post
from web.posts.serializers.post_serializer import PostSerializer


class CustomizedSearchViewSet(mixins.ListModelMixin, GenericViewSet):

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        country = self.request.query_params.get('country', None)
        state = self.request.query_params.get('state', None)
        city = self.request.query_params.get('city', None)
        route = self.request.query_params.get('route', None)
        kind = self.request.query_params.get('kind', None)
        max_price = self.request.query_params.get('max_price', None)

        filter_criteria = Q(is_expired=False)
        if kind:
            filter_criteria &= Q(kind=kind)
        if max_price:
            filter_criteria &= Q(demanded_price__range=[0, max_price])
        if country:
            filter_criteria &= Q(location__country=country)
        if state:
            filter_criteria &= Q(location__state=state)
        if city:
            filter_criteria &= Q(location__city=city)
        if route:
            filter_criteria |= Q(location__route=route)

        return Post.objects.filter(filter_criteria).order_by('-id')