from django.conf.urls import url

from books import views

app_name = 'books'

urlpatterns = [
    url(r'^$', views.index, name="index"),
]

urlpatterns += [
    url(r'^books/$', views.books, name="books"),
    url(r'^authors/$', views.authors, name="authors"),
    url(r'^publishers/$', views.publishers, name="publishers"),
]

urlpatterns += [
    url(r'^book/add/$', views.book_form, name="book_form"),
    url(r'^author/add/$', views.author_form, name="author_form"),
    url(r'^publisher/add/$', views.publisher_form, name="publisher_form"),
]

urlpatterns += [
    url(r'^book/(?P<book_id>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^author/(?P<author_id>[0-9]+)/$', views.author_detail, name='author_detail'),
    url(r'^publisher/(?P<publisher_id>[0-9]+)/$', views.publisher_detail, name='publisher_detail'),
]

urlpatterns += [
    url(r'^books/delete/$', views.item_delete, name='delete_book'),
    url(r'^authors/delete/$', views.item_delete, name='delete_author'),
    url(r'^publishers/delete/$', views.item_delete, name='delete_publisher'),
]
