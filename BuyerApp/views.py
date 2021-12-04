
#Django imports
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from AuthApp.models import User
from BookApp.models import Book
from BuyerApp.models import Cart

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

#RestImports
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView, ListAPIView,UpdateAPIView,DestroyAPIView
from rest_framework import generics,mixins
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from rest_framework import permissions
from rest_framework.filters import SearchFilter,OrderingFilter


#Serializers
from BuyerApp.serializers import (CartSerializer)

class AddCartView(CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

