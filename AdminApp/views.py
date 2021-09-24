
#Django imports
from django.contrib.auth import get_user_model
from django.shortcuts import render
from AuthApp.models import User

#RestImports
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework import serializers, status

#Serializers
from AdminApp.serializers import UpdateUserSerializer,UserViewSerializer


User = get_user_model()
class AdminUserView(APIView):
    
    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserViewSerializer(snippets, many=True)
        return Response(serializer.data)
    
class sellerUserView(APIView):
    
    def get(self, format=None):
        snippets = User.objects.filter(ROLE='seller')
        print(snippets)
        serializer = UserViewSerializer(snippets, many=True)
        return Response(serializer.data)
    
class BuyerUserView(APIView):
    
    def get(self,format=None):
        snippets = User.objects.filter(ROLE='buyer')
        serializer = UserViewSerializer(snippets, many=True)
        return Response(serializer.data)
    
class DonarUserView(APIView):
    
    def get(self, format=None):
        snippets = User.objects.filter(ROLE='donar')
        serializer = UserViewSerializer(snippets, many=True)
        return Response(serializer.data)
    
    
class UpdateProfileView(UpdateAPIView,ListAPIView,):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

    def get(self, request,pk, format=None):
        
        try:
            User.objects.get(pk=pk)
            snippets = User.objects.filter(pk=pk)
            serializer = UpdateUserSerializer(snippets, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
 
        except User.DoesNotExist:
            return Response({'status': False,'message':'User not found'},
                            status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self, pk, format=None):
        try:
            User.objects.get(pk=pk)
            snippets = User.objects.filter(pk=pk)
        
            snippets.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
 
        except User.DoesNotExist:
            return Response({'status': False},
                            status=status.HTTP_400_BAD_REQUEST) 
        