from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'', views.EmployeesPayrollViewset, base_name='users')

urlpatterns = [
    url(r'^payslip/review/(?P<pk>\d+)$', views.ReviewPayslipView.as_view(), name="review_payslip"),
    url(r'^payslip/confirm/$', views.ConfirmPayslipView.as_view(), name='bulk_confirm_payslip'),
    url(r'payslip/', include(router.urls))
]
