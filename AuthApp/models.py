#from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, NullBooleanField
from phone_field import PhoneField


# Create your models here.
class Interest(models.Model):
    Interest=models.CharField(max_length=20,primary_key=True,blank=False)
    def __str__(self):
        return self.Interest

class User(AbstractUser):
    # phone = PhoneField(blank=True, help_text='Contact phone number')
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
    email = models.EmailField(max_length=254, unique=True)
    # interests=models.OneToOneField(Interest,on_delete=models.CASCADE,null=True,blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def is_upperclass(self):
        return self.ROLE in {self.SELLER, self.BUYER, self.DONAR, self.ADMIN}
    
    def __str__(self):
        return str(self.email)
    