from django.db import models
from main.models import Book, User

# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)