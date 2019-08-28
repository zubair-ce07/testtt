"""freelancing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

from accounts.api import views as user_views
from dashboard.api import views as buyer_views
from seller.api import views as seller_views

urlpatterns = [
    # api
    url(r'^api/v1/api-token-auth/', obtain_auth_token),
    url(r'^api/v1/change-role/', user_views.UserRolesApi.as_view()),
    url(r'^api/v1/register/$', user_views.UserApiCreate.as_view()),
    url(r'^api/v1/users/$', user_views.UserApiList.as_view()),
    url(r'^api/v1/profile/$', user_views.UserProfileApi.as_view()),
    url(
        r'^api/v1/users/(?P<pk>[0-9]+)$',
        user_views.UserDetailsApi.as_view()
    ),
    url(
        r'^api/v1/requests/$',
        buyer_views.RequestApi.as_view()
    ),
    url(
        r'^api/v1/requests/(?P<pk>[0-9]+)$',
        buyer_views.RequestDetailsApi.as_view()
    ),
    url(
        r'^api/v1/request_files/$',
        buyer_views.RequestFilesApi.as_view()
    ),
    url(
        r'^api/v1/request_files/(?P<pk>[0-9]+)$',
        buyer_views.RequestFilesDetailsApi.as_view()
    ),
    url(
        r'^api/v1/gigs/$',
        seller_views.GigApi.as_view()
    ),
    url(
        r'^api/v1/gigs/(?P<pk>[0-9]+)$$',
        seller_views.GigDetailsApi.as_view()
    ),
    url(
        r'^api/v1/gig_gallery/$',
        seller_views.GalleryFilesApi.as_view()
    ),
    url(
        r'^api/v1/gig_gallery/(?P<pk>[0-9]+)$$',
        seller_views.GalleryFilesDetailsApi.as_view()
    ),
    url(
        r'^api/v1/offers/$',
        seller_views.OffersApi.as_view()
    ),
    url(
        r'^api/v1/offers/(?P<pk>[0-9]+)$$',
        buyer_views.OfferDetailsApi.as_view()
    ),


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
