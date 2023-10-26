from django.db import models
from main.models import User
from booksdatabase.models import Book

# Create your models here.
class Report(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.book.title} by {self.user.username}"