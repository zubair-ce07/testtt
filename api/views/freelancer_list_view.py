from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from api.Serializers.user_serializer import UserSerializer


class ListFreelancerView(ListAPIView):
    queryset = User.objects.filter(groups__name="Freelancer")
    serializer_class = UserSerializer
