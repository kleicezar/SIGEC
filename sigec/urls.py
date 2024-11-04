from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('config.urls')),
    # path('', include('users.urls')),
    # path('', include('Registration.urls'))
    # path('', include('Products.urls'))
    # path('', include('Sale.urls'))
    # path('', include('login.urls')), # ainda é preciso criar usuarios primeiro
    ]
