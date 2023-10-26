from django.db import models
from main.models import *
from booksdatabase.models import *

# Create your models here.
class MyBook(models.model):
    User = models.ForeignKey(User, on_delete= models.CASCADE)
    Book = models.ForeignKey(Book, on_delete= models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    review = models.TextField()