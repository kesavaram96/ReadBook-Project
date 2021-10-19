from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('auth/',include('AuthApp.urls')),
    path('admin/',include('AdminApp.urls')),
    path('seller/',include('SellerApp.urls')),
    path('buyer/',include('BuyerApp.urls')),
    path('donar/',include('DonarApp.urls')),
    
    
]
