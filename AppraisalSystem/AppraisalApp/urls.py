from django.urls import path
from . import views

app_name = 'appraisal'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('home/', views.Home.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('edit_profile/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('employees/', views.EmployeeView.as_view(), name='employees'),
    path('employee_detail/<int:pk>', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('send_feedback/<int:emp_id>', views.SendFeedbackView.as_view(), name='send_feedback'),
    path('edit_feedback/<int:feedback_id>', views.EditFeedbackView.as_view(), name='edit_feedback'),
    path('<int:feedback_id>/delete_feedback', views.DeleteFeedbackView.as_view(), name='delete_feedback'),

]
