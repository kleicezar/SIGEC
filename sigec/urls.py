from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')), # ainda é preciso criar usuarios primeiro
    path('', include('config.urls')),
    path('', include('Sale.urls')),
    # path('', include('Registry.urls')),
    # path('', include('users.urls')),
    # path('', include('Products.urls')),
    ]
