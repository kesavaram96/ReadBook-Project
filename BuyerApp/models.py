from django.db import models

from AuthApp.models import User
from BookApp.models import Book
from decimal import Decimal

# Create your models here.

class Bought(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    payment=models.CharField(max_length=50,blank=True)
    
    def __str__(self):
        return str(self.book)
    
class Cart(models.Model):
    date = models.DateTimeField(auto_now_add=True,null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),null=True)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    NumberOfItem=models.IntegerField()
    
    def __str__(self):
        return str(self.book)
    
    # @property
    # def book(self):
    #     return self.book.Name