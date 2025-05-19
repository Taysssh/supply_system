from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contracts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', lambda _: redirect('/admin/')),  # Редирект на админку
]