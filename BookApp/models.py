#from typing_extensions import Required
from django.db import models
# from django.db.models.fields import CharField, NullBooleanField
# from phone_field import PhoneField
from AuthApp.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

def year_choices():
    return [(r,r) for r in range(1700, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

class Author(models.Model):
    Name=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return str(self.Name)
    
class Publisher(models.Model):
    Name=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return str(self.Name)
    


class Book(models.Model):
        
    novels='novels'
    stories='stories'
    short_stories='short_stories'
    comics='comics'
    science='science'
    education='education'
    language_lit='language_lit'
    biography='biography'

    Catogory=[
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
    
    Catogory=models.CharField(
        max_length=15,
        choices=Catogory,
        default=novels,
    )
    
    Name=models.CharField(max_length=150,blank=False,null=True)
    ISBN10=models.BigIntegerField(null=True)
    ISBN13=models.BigIntegerField(null=True)
    Author=models.ManyToManyField(Author)
    PublicationDate=models.IntegerField(choices=year_choices(), default=current_year,null=True)
    Publisher=models.ManyToManyField(Publisher,blank=True)
    Rating=models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],null=True)
    CopyRightInfo=models.TextField(blank=True,null=True)
    NumberOfCopy=models.IntegerField(blank=True,null=True)
    Caption=models.CharField(max_length=50)
    Description=models.TextField(blank=False,null=True)
    Length=models.IntegerField(blank=True, help_text='Weight of the book per Grams',null=True)
    GOOD='good'
    DAMAGED='damaged'
    
    ConditionChoice= [
        (GOOD,'good'),
        (DAMAGED,'damaged')
    ]
    
    OLD='old'
    NEW='new'
    
    QualityChoice= [
        (NEW,'new'),
        (OLD,'old')
    ]
    Condition=models.CharField(max_length=8,choices=ConditionChoice,blank=True)
    Quality=models.CharField(max_length=3,choices=QualityChoice,blank=True)
    
    A5='A5'
    A4='A4'
    A3='A3'
    A2='A2'
    A1='A1'
    B3='B3'
    b5='b5'
    Section_ofSize=[
        (A5,'A5'),
        (A4,'A4'),
        (A3,'A3'),
        (A2,'A2'),
        (A1,'A1'),
        (B3,'B3'),
        (b5,'b5'),
    ]
    Size=models.CharField(max_length=8,choices=Section_ofSize,default=A5)
    Price=models.DecimalField(max_digits=10,help_text='Price in LKR',decimal_places=2,null=True)
    # Price=models.FloatField()
    FrontCover=models.ImageField(upload_to=None,blank=False,null=False,help_text='Front cover page Image of the book')
    BackCover=models.ImageField(upload_to=None,blank=True,help_text='Back cover page Image of the book')
    FirstPage=models.ImageField(upload_to=None,blank=True,help_text='First page Image of the book')
    Body2nd=models.ImageField(upload_to=None,blank=True,help_text='Body 2nd page Image of the book')
    PageInside=models.ImageField(upload_to=None,blank=True,help_text='page inside Image of the book')
    DamagedPart=models.ImageField(upload_to=None,blank=True,help_text='Damaged page Image of the book')
    
    Seller=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    is_free=models.BooleanField(default=False)
    for_sale=models.BooleanField(default=True)
    
    is_available=models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.Name)
    
