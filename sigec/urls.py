from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')), 
    path('', include('config.urls')),
    path('', include('sale.urls')),
    path('', include('registry.urls')),
    path('', include('purchase.urls')),
    path('', include('finance.urls')),
    path('',include('service.urls')),

]
