# files/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('files/edit/<int:pk>/', views.file_edit, name='file_edit'),
    path('files/edit/<int:pk>/save/', views.save_file_data, name='save_file_data'),
    path('files/create/', views.file_edit, name='file_create'),
]
