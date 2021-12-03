from logging import exception
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from django.db import transaction

from BookApp.models import Book,Author,Publisher
from BuyerApp.models import Bought
from AuthApp.models import User,AddressBook



User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields =('Name',)
        
class PublisherSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Publisher
        fields = ('Name',)
 
class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields ='__all__'
     
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('id','first_name', 'email','ROLE','phone_no')
        
class UpdateUserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=False, allow_blank=True, )
    # password_confirmation = serializers.CharField(max_length=50,write_only=True)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
    class Meta:
        model = User
        fields = ('email','id', 
                  'first_name', 'last_name', 
                  'ROLE','interests','phone_no',
                 )
    def update(self, instance,validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.ROLE = validated_data['ROLE']
        instance.phone_no = validated_data['phone_no']
        instance.interests = validated_data['interests']
        

        instance.save()

        return instance
        
    
    

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(max_length=50,write_only=True)
    
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({'password_confirmation': _("The two password fields didn't match.")})
        return data
            
    @transaction.atomic()
    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        role = validated_data['ROLE']
        email = validated_data['email']
        interests=validated_data['interests']
        phone_no=validated_data['phone_no']
        is_superuser=validated_data['is_superuser']
        is_staff=validated_data['is_staff']
        
        
        
        
        if validated_data['password']!=validated_data['password_confirmation']:
            raise serializers.ValidationError('Password must be same')
        else:
            user = User.objects.create(first_name=first_name,last_name=last_name,
                                       ROLE=role,email=email,interests=interests,phone_no=phone_no,
                                       is_staff=is_staff,is_superuser=is_superuser)
            user.set_password(validated_data['password'])
            user.save()
            return user
            

    class Meta:
        model = User
        fields = ('email','password', 
                  'first_name', 'last_name', 
                  'ROLE','password_confirmation','interests','phone_no',
                  'is_superuser','is_staff'
                 )
        extra_kwargs={'password':{'write_only':True}}
        non_native_fields = ('password_confirmation',)


class AdminProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=('email','first_name','last_name','ROLE','phone_no','is_super','is_staff')

    def update(self, instance,validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.ROLE = validated_data['ROLE']
        instance.phone_no = validated_data['phone_no']
        instance.is_super = validated_data['is_super']
        instance.is_staff = validated_data['is_staff']

        instance.save()

        return instance
    
class BookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=('id','Name','Caption','Price','Seller','Rating')

class BookListSerializer(serializers.ModelSerializer):
    Author=AuthorSerializer(many=True,required=False)
    Publisher=PublisherSerializer(many=True)
    class Meta:
        model=Book
        fields='__all__'

class SellerUploads(serializers.ModelSerializer):

    class Meta:
        model=Book
        fields=('Name','Seller','Caption','FrontCover','Price')

class BoughtSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Bought
        fields='__all__'
        
class AddBookSerializer(serializers.ModelSerializer):
    Author=AuthorSerializer(many=True,required=False)
    Publisher=PublisherSerializer(many=True)
    class Meta:
        model=Book
        fields='__all__'
        
    def create(self, validated_data):
        author_data = validated_data.pop('Author')
        publisher_data = validated_data.pop('Publisher')
        user = self.context['request'].user
        
        
        group = Book.objects.create(**validated_data)
        
        for author in author_data:
            d=dict(author)
            if Author.objects.filter(Name=d['Name']).exists():
                au=Author.objects.get(Name=d['Name'])
                if au:
                    group.Author.add(au)
            else:
                Author.objects.create(Name=d['Name'])
                au=Author.objects.get(Name=d['Name'])
                if au:
                    group.Author.add(au)
        for publisher in publisher_data:
            d=dict(publisher)
            if Publisher.objects.filter(Name=d['Name']).exists():
                au=Publisher.objects.get(Name=d['Name'])
                if au:
                    group.Author.add(au)
            else:
                Publisher.objects.create(Name=d['Name'])
                au=Publisher.objects.get(Name=d['Name'])
                if au:
                    group.Publisher.add(au)    
        return group

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=('Rating')
        
    def update(self, instance,validated_data):
        instance.Rating = validated_data['Rating']
        instance.save()
        return instance
    
    