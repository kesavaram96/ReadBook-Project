
#Django imports
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from django.http import HttpResponse
from AuthApp.models import User
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
from AdminApp.serializers import (UpdateUserSerializer,
                                  UserViewSerializer,
                                  AdminProfileSerializer,
                                  UserCreateSerializer,
                                  BookViewSerializer,
                                  BoughtSerializer,
                                  SellerUploads,
                                  BookListSerializer,
                                  AddBookSerializer,
                                  SalesSerializer)
#Python import
import csv

#localimport
from AuthApp.utils import generate_jwt_token
from BookApp.models import Book,Sales
from BuyerApp.models import Bought

User = get_user_model()

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        try:
            request.user
            return bool(request.user and request.user.ROLE=='admin' and request.user.is_superuser)
        except:
            redirect('auth/login')
        
    
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
            snippets2 = Book.objects.filter(Seller=pk)
            
            serializer = UpdateUserSerializer(snippets, many=True)
            serializer2=BookViewSerializer(snippets2,many=True)
            
            return Response({'User':serializer.data,'Sales':serializer2.data},status=status.HTTP_200_OK)
 
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
    
class BuyerUserView(generics.ListAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    queryset = User.objects.filter(ROLE='buyer')
    serializer_class = UserViewSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['email','first_name']
  
    
    # def get(self,format=None):
    #     snippets = User.objects.filter(ROLE='buyer')
    #     serializer = UserViewSerializer(snippets, many=True)
    #     return Response(serializer.data)

class BuyerUpdateView(ListAPIView,DestroyAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = UpdateUserSerializer
    queryset = User.objects.filter(ROLE='buyer')
    
    
    def get(self, request,pk, format=None):
        
        try:
            User.objects.get(pk=pk,ROLE='buyer')
            snippets = User.objects.filter(pk=pk,ROLE='buyer')
            snippets2=Bought.objects.filter(buyer=pk)
            serializer = UpdateUserSerializer(snippets, many=True)
            serializer2 = BookViewSerializer(snippets2, many=True)
            
            return Response({'User':serializer.data,'Books':serializer2.data},status=status.HTTP_200_OK)
 
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
    permission_classes = (IsSuperUser,IsAuthenticated)
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
                             'message': str('Error')},
                            status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserCreateSerializer(snippets, many=True)
        return Response(serializer.data)


class adminProfileView(ListAPIView,UpdateAPIView,DestroyAPIView):
    # permission_classes = (IsSuperUser,IsAuthenticated)
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
    
class sellerUploadView(APIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    def get(self,format=None):
        snippets = Book.objects.all().order_by('Upload_Date').reverse()
        serializer = SellerUploads(snippets, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        pass
    
class BoughtView(APIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    def get(self,format=None):
        snippets = Bought.objects.all()
        serializer = BoughtSerializer(snippets, many=True)
        return Response(serializer.data)

class ProductView(APIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    def get(self,format=None):
        snippets = Book.objects.all()
        serializer = BookViewSerializer(snippets, many=True)
        return Response(serializer.data)
    

class BookListView(generics.ListAPIView,generics.ListCreateAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = '__all__'
    
class ProductUpdateView(ListAPIView,DestroyAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = BookListSerializer
    queryset = Book.objects.all()
    
    
    def get(self, request,pk, format=None):
        
        try:
            Book.objects.get(pk=pk)
            snippets = Book.objects.filter(pk=pk)
            serializer = BookListSerializer(snippets, many=True)
            
            return Response(serializer.data,status=status.HTTP_200_OK)
 
        except Book.DoesNotExist:
            return Response({'status': False,'message':'Product not found'},
                            status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
            
    
class AddProductsView(CreateAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    serializer_class = AddBookSerializer
    queryset = Book.objects.all()
    
class ExportCSVView(APIView):
    serializer_class = SellerUploads
    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=True,
        )
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        
        serializer = self.get_serializer(
            Book.objects.all(),
            many=True
        )
        header = SellerUploads.Meta.fields
        
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        
        return response
class ReviewProductView(APIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    def get(self,request,pk):
        try:
            book=Book.objects.get(pk=pk)
            book.is_publish=True
            book.save()
            return Response({'Message':'Book published'},status=status.HTTP_200_OK)
 
        except Book.DoesNotExist:
            return Response({'status': False,'message':'Book not found'},
                            status=status.HTTP_400_BAD_REQUEST) 
            

class SalesView(generics.ListAPIView):
    permission_classes = (IsSuperUser,IsAuthenticated)
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = '__all__'