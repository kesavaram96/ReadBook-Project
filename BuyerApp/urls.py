from django.urls import path,include
from .views import AddCartView
urlpatterns = [
    path('add-cart/<int:pk>/',AddCartView.as_view()),
    ]