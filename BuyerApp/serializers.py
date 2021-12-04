from logging import exception
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from django.db import transaction

from BookApp.models import Book,Author,Publisher
from BuyerApp.models import Bought,Cart
from AuthApp.models import User,AddressBook



User = get_user_model()

class CartSerializer(serializers.ModelSerializer):
    
    @transaction.atomic()   
    def create(self,validated_data):
        user = self.context['request'].user
        ItemNumber=validated_data['NumberOfItem']
        book=Book.objects.get(id=13)
        total_price=book.Price*ItemNumber
        data=Cart.objects.create(NumberOfItem=ItemNumber,buyer=user,book=book,total_price=total_price)
        data.save()
        return data
    
    class Meta:
        model = Cart
        fields = ('NumberOfItem',)
        
