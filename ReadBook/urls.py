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
admin.site.site_header="ReadBook Admin Page"
admin.site.site_title="ReadBook Admin Page"
admin.site.index_title="Welcome back to ReadBook Admin Page"
