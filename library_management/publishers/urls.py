from django.urls import path

from . import views

app_name = 'publishers'
urlpatterns = [
    path('publishers/', views.PublisherList.as_view(),
         name='publishers-index'),
    path('publishers_data_list/',
         views.PublisherDataList.as_view(),
         name='publishers-data-index'),
    path('publisher/<int:pk>/',
         views.PublisherDetail.as_view(),
         name='publisher-detail'),
    path('publisher/<int:pk>/delete',
         views.PublisherDestroy.as_view(),
         name='publisher-delete'),
    path('publisher/<int:pk>/update',
         views.PublisherUpdate.as_view(),
         name='publisher-update'),
    path('publisher/<int:pk>/books/',
         views.PublisherBooksList.as_view(),
         name='publisher-books'),
]
