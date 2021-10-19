
#Django imports
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from AuthApp.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

#RestImports
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView, GenericAPIView, ListAPIView,UpdateAPIView,DestroyAPIView
from rest_framework import generics,mixins
from rest_framework.response import Response
from rest_framework import serializers, status

from rest_framework.permissions import IsAuthenticated 
from rest_framework import permissions


#Serializers
from AdminApp.serializers import (UpdateUserSerializer,
                                  UserViewSerializer,
                                  AdminProfileSerializer,
                                  UserCreateSerializer)

#localimport
from AuthApp.utils import generate_jwt_token


User = get_user_model()

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.ROLE=='admin' and request.user.is_superuser)
    

class AdminUserView(generics.ListAPIView,):
    permission_classes = (IsSuperUser,IsAuthenticated)
    
    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserViewSerializer(snippets, many=True)
        return Response(serializer.data)
    
class sellerUserView(APIView):
    
    permission_classes = (IsSuperUser,IsAuthenticated)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'email']
    def get(self,request, format=None):
        snippets = User.objects.filter(ROLE='seller') 
        serializer = UserViewSerializer(snippets, many=True)
        return Response(serializer.data)
    
# @method_decorator(csrf_exempt, name='dispatch')
class sellerUpdateView(UpdateAPIView,DestroyAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.filter(ROLE='seller')
    
    
    def get(self, request,pk, format=None):
        
        try:
            User.objects.get(pk=pk,ROLE='seller')
            snippets = User.objects.filter(pk=pk,ROLE='seller')
            serializer = UpdateUserSerializer(snippets, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
 
        except User.DoesNotExist:
            return Response({'status': False,'message':'User not found'},
                            status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
            
    def update(self, request,pk, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateUserSerializer(
            instance=instance,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class BuyerUserView(APIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    def get(self,format=None):
        snippets = User.objects.filter(ROLE='buyer')
        serializer = UserViewSerializer(snippets, many=True)
        return Response(serializer.data)

class BuyerUpdateView(ListAPIView,DestroyAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.filter(ROLE='seller')
    
    
    def get(self, request,pk, format=None):
        
        try:
            User.objects.get(pk=pk,ROLE='seller')
            snippets = User.objects.filter(pk=pk,ROLE='seller')
            serializer = UpdateUserSerializer(snippets, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
 
        except User.DoesNotExist:
            return Response({'status': False,'message':'User not found'},
                            status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
            
    def update(self, request,pk, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateUserSerializer(
            instance=instance,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


class DonarUserView(APIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    def get(self,format=None):
        snippets = User.objects.filter(ROLE='donar')
        serializer = UserViewSerializer(snippets, many=True)
        return Response(serializer.data)
    
class DonarUpdateView(UpdateAPIView,ListAPIView,DestroyAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.filter(ROLE='donar')
    
    
    def get(self, request,pk, format=None):
        
        try:
            User.objects.get(pk=pk,ROLE='donar')
            snippets = User.objects.filter(pk=pk,ROLE='donar')
            serializer = UpdateUserSerializer(snippets, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
 
        except User.DoesNotExist:
            return Response({'status': False,'message':'User not found'},
                            status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
            
    def update(self, request,pk, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateUserSerializer(
            instance=instance,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
              

class UpdateProfileView(UpdateAPIView,ListAPIView,):
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

    def get(self, request,pk, format=None):
        
        try:
            User.objects.get(pk=pk)
            snippets = User.objects.filter(pk=pk,ROLE='admin')
            serializer = UpdateUserSerializer(snippets, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
 
        except User.DoesNotExist:
            return Response({'status': False,'message':'User not found'},
                            status=status.HTTP_400_BAD_REQUEST) 
    
    def get_object(self):
        return self.request.id
    
    def delete(self, pk, format=None):
        try:
            User.objects.get(pk=pk)
            snippets = User.objects.filter(pk=pk)
        
            snippets.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
 
        except User.DoesNotExist:
            return Response({'status': False},
                            status=status.HTTP_400_BAD_REQUEST) 


class UserCrateView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = (IsSuperUser,IsAuthenticated)
   

    __doc__ = "Registration API for user"

    def post(self, request, *args, **kwargs):
        try:
            user_serializer = UserCreateSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                data = generate_jwt_token(user, user_serializer.data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in user_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': False,
                             'message': str('Error')},
                            status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserCreateSerializer(snippets, many=True)
        return Response(serializer.data)


class adminProfileView(ListAPIView,UpdateAPIView,DestroyAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = AdminProfileSerializer
    queryset = User.objects.all()

    def get(self,request,format=None):
        requestUser=request.user
        snippets = User.objects.filter(email=requestUser,ROLE='admin')
        serializer = AdminProfileSerializer(snippets, many=True)
        return Response(serializer.data)
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AdminProfileSerializer(
            instance=instance,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


class UserProfileChangeAPIView(generics.RetrieveAPIView,
                               mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin):
    
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = AdminProfileSerializer
    # parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        username = self.kwargs["email"]
        obj = get_object_or_404(User, email=username)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)