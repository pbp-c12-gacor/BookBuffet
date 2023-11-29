from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from booksdatabase.models import Book

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=25)
    text = models.TextField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(default=timezone.now)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
