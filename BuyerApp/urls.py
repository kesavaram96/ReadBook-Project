from django.urls import path,include
from .views import AddCartView,CartView

urlpatterns = [
    path('cart/',CartView.as_view()),
    path('add-cart/',AddCartView.as_view()),
    ]