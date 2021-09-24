from django.urls import path,include
from .views import RegistrationAPIView,LoginView,LogoutView,ChangePasswordView
urlpatterns = [
    path('register/',RegistrationAPIView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    
    path('change-password/', ChangePasswordView.as_view()),
    
    ]