#from typing_extensions import Required
# from typing_extensions import Required
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, NullBooleanField
from phone_field import PhoneField


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20,primary_key=True,blank=False)
    def __str__(self):
        return self.name

class User(AbstractUser):
    username=None
    phone_no = PhoneField(blank=True, help_text='Contact phone number',null=True, unique=True)
    SELLER = 'seller'
    BUYER = 'buyer'
    DONAR = 'donar'
    ADMIN = 'admin'
    ROLE = [
        (SELLER, 'seller'),
        (BUYER, 'buyer'),
        (DONAR, 'donar'),
        (ADMIN, 'admin'),
    ]
    ROLE = models.CharField(
        max_length=6,
        choices=ROLE,
        default=BUYER,
    )
    
    novels='novels'
    stories='stories'
    short_stories='short_stories'
    comics='comics'
    science='science'
    education='education'
    language_lit='language_lit'
    biography='biography'

    interests=[
        (novels,'novels'),
        (stories,'stories'),
        (short_stories,'short_stories'),
        (comics,'comics'),
        (science,'science'),
        (science,'science'),
    (education,'education'),
    (language_lit,'language_lit'),
    (biography,'biography'),
    ]
    
    interests=models.CharField(
        max_length=15,
        choices=interests,
        default=novels,
    )
    
    
    
    email = models.EmailField(max_length=254, unique=True)
    # interests=models.OneToOneField(Category,on_delete=models.CASCADE,null=True,blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def is_upperclass(self):
        return self.ROLE in {self.SELLER, self.BUYER, self.DONAR, self.ADMIN}
    
    def __str__(self):
        return str(self.email)
    

class AddressBook(models.Model):
    user=models.ForeignKey(User,null=True,blank=False, on_delete=models.CASCADE)
    Name=models.CharField(max_length=100,blank=True,null=True)
    AddressLine1=models.CharField(max_length=200,blank=True,null=True)
    AddressLine2=models.CharField(max_length=200,blank=True,null=True)
    Country=models.CharField(max_length=200,blank=True,null=True)
    ZipCode=models.CharField(max_length=100,blank=True,null=True)
    City=models.CharField(max_length=100,blank=True,null=True)
    State_province=models.CharField(max_length=100,blank=True,null=True)
    Is_Default=models.BooleanField()
    Phone = PhoneField(blank=True, help_text='Contact phone number',unique=False)
    AddressType=models.CharField(max_length=100,blank=True,null=True)