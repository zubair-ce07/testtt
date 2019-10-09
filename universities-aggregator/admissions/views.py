# Create your views here.


from rest_framework import viewsets
from .serializers import ProgramSerializer
from .models import Program


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
