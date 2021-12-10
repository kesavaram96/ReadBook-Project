from logging import exception
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from django.db import transaction

from BookApp.models import Book,Author,Publisher
from BuyerApp.models import Bought,Cart
from AuthApp.models import User,AddressBook

from rest_framework.fields import CurrentUserDefault

User = get_user_model()

class AddCartSerializer(serializers.ModelSerializer):
     
    def validate(self,data):
        book=data['book']
        Num=data['NumberOfItem']
        
        obj=Book.objects.get(Name=book)
        p=obj.NumberOfCopy

        if Num>p:
            Item=str(p)
            Message="Number of Books available is "+Item
            raise serializers.ValidationError({'Error':Message})
        else:
            return data
    

    def create(self,validated_data):
        user = validated_data['buyer']
        book=validated_data['book']
        ItemNumber=validated_data['NumberOfItem']

        obj=Book.objects.get(id=book.id)
        price=obj.Price
        total=price*ItemNumber
        
        data=Cart.objects.create(book=book,NumberOfItem=ItemNumber,
                                 total_price=total,buyer=user)
        data.save()
        
        return data
    
    class Meta:
        model = Cart
        fields =('NumberOfItem','book',)
        
class CartSerializer(serializers.ModelSerializer):
        class Meta:
            model = Cart
            fields ='__all__'