from .views import EmployeeRUDView, EmployeeListView, CompetencyListView, CompetencyRetrieveView, CompetencyCreateView, \
    FeedbackCreateView
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('emp_rud/<int:pk>', EmployeeRUDView.as_view(), name='employee_rud'),
    path('emp_list/', EmployeeListView.as_view(), name='employee_list'),
    path('competency_list/', CompetencyListView.as_view(), name='competency_list'),
    path('competency/<int:pk>', CompetencyRetrieveView.as_view(), name='competency_retrieve'),
    path('competency_create/', CompetencyCreateView.as_view(), name='competency_create'),
    path('feedback_create/', FeedbackCreateView.as_view(), name='feedback_create'),
]
