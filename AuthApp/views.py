# python imports
import requests

# Django imports
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError  
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import get_user_model,logout,login,authenticate
from django.http import Http404
# from django.contrib.auth import logout

# Rest Framework imports
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
# from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView

from rest_framework import generics
from django.contrib.auth.models import User,auth
from rest_framework.permissions import IsAuthenticated   


#Local imports
from .serializers import UserCreateSerializer,JSONWebTokenSerializer,ChangePasswordSerializer
from .models import User
from AuthApp.utils import generate_jwt_token




User = get_user_model()
#---------------User registration view--------------------
class RegistrationAPIView(APIView):
    serializer_class = UserCreateSerializer

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
                             'message': str('Password must be same')},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserCreateSerializer(snippets, many=True)
        return Response(serializer.data)
    
#---------------------User login view-------------------------------
class LoginView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer
    
    __doc__ = "Log In API for user which returns token"

    @staticmethod
    def post(request):
        try:
            serializer = JSONWebTokenSerializer(data=request.data)
            if serializer.is_valid():
                serialized_data = serializer.validate(request.data)
                
                # print(re)
                user = User.objects.get(email=request.data.get('email'))
                usertype=user.ROLE
                
                #ownrisk
                username = request.data.get('email')
                password = request.data.get('password')
                user = authenticate(request, email=username, password=password)
                if user is not None:
                    login(request, user)
               

                return Response({
                    'status': True,
                    'token': serialized_data['token'], 
                    'role':usertype,
                }, status=status.HTTP_200_OK)
                    
            else:
                message = ''
                for error in serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "User doesnot exists"},
                            status=status.HTTP_400_BAD_REQUEST)
            
#--------user_logoutView------------------------------------------
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    @staticmethod
    def post(request):
        """
        Logout API for user
        """
        try:
            user = request.data.get('user', None)
            print(user)
            logout(request)
            return Response({'status': True,
                             'message': "logout successfully"},
                            status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False},
                            status=status.HTTP_400_BAD_REQUEST)
    




#---------Change_password----------------------------------------
class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'message':'Password Sucessfully updated'}, status=status.HTTP_200_OK)
        
    
