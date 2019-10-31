"""Books app url paths."""
from django.urls import path
from books import views


urlpatterns = [
    path('book-home/', views.BooksListView.as_view(), name='book-home'),
    path('new/', views.BookCreateView.as_view(), name='book-create'),
    path('detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    path('delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
    path('issue/<int:pk>/', views.BookIssueView.as_view(), name='book_issue'),
    path('user_information/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('request/<int:pk>/', views.BookRequestView.as_view(), name='book_request'),
    path('user_books/<int:pk>/', views.IssueBookListView.as_view(), name='user_books'),
    path('user_requests/<int:pk>/', views.UserRequestsListView.as_view(), name='user_requests'),
    path('issuebook_delete/<int:pk>/', views.IssuebookDeleteView.as_view(), name='isuebook_delete'),
    path('request_delete/<int:pk>/', views.RequestbookDeleteView.as_view(), name='requests_delete'),
    path('user_books/1/', views.MyIssuedBooks.as_view(), name='my_books'),
    path('user_requests/1/', views.RequestView.as_view(), name='direct_requests'),
]
