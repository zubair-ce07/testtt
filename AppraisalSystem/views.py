from rest_framework import viewsets
from AppraisalApp import models
from .serializers import EmployeeSerializer, CompetencyFeedbackSerializer
from .permissions import IsManagerOfEmplyee


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = EmployeeSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = models.Feedback.objects.all()
    serializer_class = CompetencyFeedbackSerializer
    permission_classes = [IsManagerOfEmplyee]

