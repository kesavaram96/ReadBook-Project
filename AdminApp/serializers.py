from logging import exception
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
User = get_user_model()

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

    # def validate_email(self, value):
    #     # user = self.context['request'].user
    #     user=get_object()
    #     if User.objects.exclude(email=user.email).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})
    #     return value

    # def validate_username(self, value):

    #     # user = self.context['request'].user
    #     if User.objects.exclude(username=value).filter(username=value).exists():
    #         raise serializers.ValidationError({"username": "This username is already in use."})
    #     return value
        

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
        
        
        
        if validated_data['password']!=validated_data['password_confirmation']:
            raise serializers.ValidationError('Password must be same')
        else:
            user = User.objects.create(first_name=first_name,last_name=last_name,
                                       ROLE=role,email=email,interests=interests,phone_no=phone_no)
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
        fields=('email','first_name','last_name','ROLE','phone_no')

    def update(self, instance,validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.ROLE = validated_data['ROLE']
        instance.phone_no = validated_data['phone_no']

        instance.save()

        return instance
    

