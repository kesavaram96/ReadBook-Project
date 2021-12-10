
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
from BuyerApp.serializers import (CartSerializer,AddCartSerializer)

class AddCartView(APIView):
    serializer_class = AddCartSerializer
    queryset = Cart.objects.all()
    permission_classes = (IsAuthenticated,)
    
    @staticmethod
    def post(request):
        try:
            data_serializer = AddCartSerializer(data=request.data)
            if data_serializer.is_valid():
                data_serializer.save(buyer=request.user)
                return Response({'status': True,'message':"Item sucessfully added to the cart"},status=status.HTTP_200_OK)
            else:
                message = ''
                for error in data_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        
            
class CartView(ListAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get(self,request,format=None):
        requestUser=request.user
        snippets = Cart.objects.filter(buyer=requestUser)
        serializer = CartSerializer(snippets, many=True)
        return Response(serializer.data)