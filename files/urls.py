# files/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.file_list, name='file_list'),
    path('edit/<int:pk>/', views.file_edit, name='file_edit'),
    path('edit/<int:pk>/save/', views.save_file_data, name='save_file_data'),
    path('create/', views.file_edit, name='file_create'),
]
