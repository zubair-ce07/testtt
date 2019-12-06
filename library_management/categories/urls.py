from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='categories-index'),
    path('categories_data_list/', views.CategoryDataList.as_view(),
         name='categories-data-index'),
    path('category/', views.CategoryCreate.as_view(), name='category-create'),
    path('category/<int:pk>/',
         views.CategoryDetail.as_view(),
         name='category-detail'),
    path('category/<int:pk>/delete',
         views.CategoryDestroy.as_view(),
         name='category-delete'),
    path('category/<int:pk>/update',
         views.CategoryUpdate.as_view(),
         name='category-update'),
]
