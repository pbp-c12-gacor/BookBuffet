from django.db import models
from main.models import *
from booksdatabase.models import *

# Create your models here.

class MyBook(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    books = models.ManyToManyField(Book,related_name='books')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,  null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    review = models.TextField(default = "")
    rating = models.IntegerField(default =0)



