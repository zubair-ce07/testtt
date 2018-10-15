from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^add/owner/$', views.OwnerCreateView.as_view(), name='add_owner'),
    url(r'^add/customer/$', views.CustomerCreateView.as_view(), name='add_customer'),
    path('user/<int:pk>/', views.UserDetailsView.as_view(), name='user_details'),
    path('add/saloon/', views.SaloonCreateView.as_view(), name='add_saloon'),
    path('saloon/<int:pk>/', views.SaloonDetailsView.as_view(), name='saloon_details'),
    path('saloons/', views.SaloonListView.as_view(), name='saloon_list'),
    path('saloon/<int:pk>/add/emp/', views.EmployeeCreateView.as_view(), name='add_employee'),
    path('emp/<int:pk>/', views.EmployeeDetailsView.as_view(), name='employee_details'),
    path('saloon/employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('saloon/<int:pk>/add/feedback/', views.FeedbackCreateView.as_view(), name='saloon_feedback'),
    path('saloon/<int:pk>/feedback/', views.FeedbackListView.as_view(), name='saloon_feedback'),
    path('feedback/<int:pk>/', views.FeedbackDetailsView.as_view(), name='saloon_edit_feedback'),
    path('saloon/<int:pk>/add/appointment/', views.RequestAppointmentCreateView.as_view(), name='add_appointment'),
    path('saloon/<int:pk>/appointments/', views.SaloonAppointmentsListView.as_view(), name='appointments_list'),
    path('appointment/<int:pk>/', views.ProcessAppointmentDetailsView.as_view(), name='appointment_detail'),
    path('appointment/<int:pk>/cancel/', views.CancelAppointmentView.as_view(), name='appointment_detail'),
    path('edit/<int:pk>/profile/', views.UpdateUserProfileView.as_view(), name='edit_profile'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
