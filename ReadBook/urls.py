from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('auth/',include('AuthApp.urls')),
    path('admin/',include('AdminApp.urls'))
    
]
