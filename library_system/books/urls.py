"""Books app url paths."""
from django.urls import path
from books import views


urlpatterns = [
    path('search/', views.SearchBookView.as_view(), name='search_results'),
    path('book-home/', views.BooksListView.as_view(), name='book-home'),
    path('new/', views.BookCreateView.as_view(), name='book-create'),
    path('detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    path('delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
    path('issue/<int:book_id>/', views.BookIssueView.as_view(), name='book_issue'),
    path('user_information/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('request/<int:book_id>/', views.BookRequestView.as_view(), name='book_request'),
    path('user_books/<int:pk>/', views.IssueBookListView.as_view(), name='user_books'),
    path('user_requests/<int:pk>/', views.UserRequestsListView.as_view(), name='user_requests'),
    path('issuebook_delete/<int:book_id>/', views.IssueBookDeleteView.as_view(), name='isuebook_delete'),
    path('request_delete/<int:book_id>/', views.RequestbookDeleteView.as_view(), name='requests_delete'),
    path('user_books/', views.MyIssuedBooks.as_view(), name='my_books'),
    path('user_requests/', views.UserRequestsView.as_view(), name='direct_requests'),
    path('upload_csv', views.BooksUpload.as_view(), name="book_upload"),
]
