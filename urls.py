from django.urls import path, include
from django.contrib import admin
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contracts.urls')),
]