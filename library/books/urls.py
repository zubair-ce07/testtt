from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from books import views

urlpatterns = [
    path('', views.api_root),
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('books/<int:pk>/update', views.BookUpdateDestroy.as_view(), name='book-destroy'),

    path('issued_books/', views.IssueBookList.as_view(), name='issuebook-list'),
    path('issued_books/<int:pk>/', views.IssueBookDetail.as_view(), name='issuebook-detail'),
  
    path('book_requests/', views.RequestBookList.as_view(),name='requestbook-list'),
    path('book_requests/<int:pk>/', views.RequestBookDetail.as_view(),name='requestbook-detail'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)