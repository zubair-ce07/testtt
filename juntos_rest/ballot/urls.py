from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (BallotReadView,
                    BallotView,
                    BallotCreate,
                    BallotVote)

router = DefaultRouter()
router.register(r'', BallotReadView)

app_name = 'ballot'

urlpatterns = [
    url(r'details/(?P<pk>[0-9]+)/$', BallotView.as_view()),
    url(r'create/$', BallotCreate.as_view()),
    url(r'vote/$', BallotVote.as_view()),
    url(r'^', include(router.urls)),
]
