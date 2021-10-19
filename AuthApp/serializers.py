from __future__ import unicode_literals
from enum import unique

# Python imports.
import logging
import datetime
import calendar

# Django imports.
from django.db import transaction
from django.utils.translation import gettext_lazy as _

# Rest Framework imports.
from rest_framework import serializers

# Third Party Library imports

# local imports.
# from .models import User

##login serializer
import jwt
import requests
# from calendar import timegm
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, get_user_model,password_validation
from django.utils.translation import ugettext as _
from .compat import Serializer

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field, PasswordField
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,auth

from django.contrib.auth.hashers import make_password

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER



##--------Login_Serializer--------------------
class JSONWebTokenSerializer(Serializer):
    
    def __init__(self, *args, **kwargs):
      
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.EmailField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            newss=credentials[self.username_field]
            if User.objects.get(email=newss):
                user = authenticate(**credentials)
                
                # login(self.user)
                

                if user:
                    if not user.is_active: 
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)
                    payload = jwt_payload_handler(user) 
                    # login(self,user)
                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user,
                    }
                
                else:
                    msg = _('Invalid password')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Invalid username')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


##---------------Usercreate_Serializer-----------------
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
                 )
        extra_kwargs={'password':{'write_only':True}}
        non_native_fields = ('password_confirmation',)






class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        else:
            return self.validated_data

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user