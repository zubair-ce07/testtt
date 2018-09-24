from rest_framework import generics
from AppraisalApp import models
from .serializers import EmployeeSerializer, CompetencySerializer, FeedbackSerializer, CompetencyFeedbackSerializer


class EmployeeRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return models.Employee.objects.all()


class EmployeeListView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return models.Employee.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CompetencyListView(generics.ListAPIView):
    serializer_class = CompetencyFeedbackSerializer

    def get_queryset(self):
        return models.Competency.objects.all()


class CompetencyRetrieveView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = CompetencyFeedbackSerializer
    queryset = models.Competency.objects.all()


class CompetencyCreateView(generics.CreateAPIView):
    serializer_class = CompetencySerializer
    queryset = models.Competency.objects.all()


class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    queryset = models.Feedback.objects.all()
