from django.conf.urls import url

from .views import ChargeView, PaymentView


urlpatterns = [
    url(r'^charge/', ChargeView.as_view(), name='charge'),
    url(r'^$', PaymentView.as_view(), name='payment'),
]
