from django.db import models

from AuthApp.models import User
from BookApp.models import Book


# Create your models here.

class Bought(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    payment=models.CharField(max_length=50,blank=True)
    
    def __str__(self):
        return str(self.book)
    
class Cart(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    NumberOfItem=models.IntegerField(default=1)