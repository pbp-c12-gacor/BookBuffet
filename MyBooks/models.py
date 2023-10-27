from django.db import models
from main.models import *
from booksdatabase.models import *

# Create your models here.

class MyBook(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

class Review(models.Model):
    MyBook = models.ForeignKey(MyBook, on_delete= models.CASCADE)
    review = models.TextField()
    score = models.IntegerField()
