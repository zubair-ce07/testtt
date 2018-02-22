from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from api.Serializers.user_serializer import UserSerializer
from api.constants import Constants


class FreelancerViewSet(ModelViewSet):
    queryset = User.objects.filter(groups__name=Constants.FREELANCER_GROUP)
    serializer_class = UserSerializer
