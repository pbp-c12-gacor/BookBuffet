from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from booksdatabase.models import Book

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    text = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(default=timezone.now)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
