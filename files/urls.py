# files/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('files/edit/<int:pk>/', views.file_edit, name='file_edit'),
    path('files/edit/<int:pk>/save/', views.save_file_data, name='save_file_data'),
    path('files/create/', views.file_create, name='file_create'),
    path('files/lists/', views.file_lists, name='file_lists'),
]

handler404 = 'project.views.custom_404_view'
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
