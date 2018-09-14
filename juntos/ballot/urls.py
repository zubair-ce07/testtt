from django.urls import path
from .views import BallotView, BallotListView, BallotDetailView, vote_ballot, BallotDeleteView


app_name = 'ballot'

urlpatterns = [
    path('add/', BallotView.as_view(), name='ballot_add'),
    path('<int:id>/edit/', BallotView.as_view(), name='ballot_edit'),
    path('<int:pk>/delete/', BallotDeleteView.as_view(), name='ballot_delete'),
    path('', BallotListView.as_view(), name='ballot_list'),
    path('<int:pk>/details/', BallotDetailView.as_view(), name="ballot_details"),
    path('<int:id>/', vote_ballot, name="ballot_vote")
]