from django.urls import path,include
from .views import RegistrationAPIView,LoginView
urlpatterns = [
    path('register/',RegistrationAPIView.as_view()),
    path('login/',LoginView.as_view())
    ]