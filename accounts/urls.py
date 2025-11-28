from django.contrib import admin
from django.urls import path
# from accounts.views import admin_custom_login
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/admin/', views.admin_custom_login, name='admin_custom_login'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)