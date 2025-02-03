from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')), 
    path('', include('config.urls')),
    path('', include('Sale.urls')),
    path('', include('Registry.urls')),
    path('', include('purchase.urls')),
    path('', include('finance.urls')),
    path('',include('Service.urls')),

]
