from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^authors/$',
        views.AuthorList.as_view(),
        name='author-list'
    ),
    url(
        r'^authors/(?P<author_id>[0-9]+)/$',
        views.AuthorDetail.as_view(),
        name='author-detail'
    ),
    url(
        r'^books/$',
        views.BookList.as_view(),
        name='book-list'
    ),
    url(
        r'^books/(?P<book_id>[0-9]+)/$',
        views.BookDetail.as_view(),
        name='book-detail'
    ),
    url(
        r'^book_issue/$',
        views.BookissueList.as_view(),
        name='book-list'
    ),
    
]
