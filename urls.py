from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView

from system.views import loginUser, signupUser, logoutUser, index, \
    ManagerIndexView, EmployeeIndexView, change_password, \
    AppraisalDeleteView, AppraisalUpdateView, AppraisalCreateView

urlpatterns = [
    path('', index, name='home'),
    path('login/', loginUser, name='login'),
    path('signup/', signupUser, name='signup'),
    path('logout/', login_required(logoutUser), name='logout'),


    path('admin/', RedirectView.as_view(url='/admin'), name='admin_home'),


    path('manager/', ManagerIndexView.as_view(), name='manager_home'),
    path('manager/employee/<int:pk>', EmployeeIndexView.as_view(),
         name='view_employee'),

    path('manager/appraisal/add', AppraisalCreateView.as_view(), name='add_appraisal'),
    path('manager/apparaisal/delete/<int:pk>', AppraisalDeleteView.as_view(),
         name='delete_appraisal'),
    path('manager/apparaisal/update/<int:pk>', AppraisalUpdateView.as_view(),
         name='update_appraisal'),


    path('employee/', EmployeeIndexView.as_view(), name='employee_home'),
    path('profile/password', change_password, name='change_password')

]