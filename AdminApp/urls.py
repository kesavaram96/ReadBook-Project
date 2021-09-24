from django.urls import path,include
from .views import AdminUserView,sellerUserView,BuyerUserView,DonarUserView,UpdateProfileView

urlpatterns = [
    path('',AdminUserView.as_view()),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(),),
    
    #sellerProfileAPI
    path('seller-profile/',sellerUserView.as_view(),name='sellerview'),
    
    #BuyerProfileAPI
    path('buyer-profile/',BuyerUserView.as_view(),name='sellerview'),
    
    #DonarProfileAPI
    path('donar-profile/',DonarUserView.as_view(),name='sellerview'),
    
    
]
