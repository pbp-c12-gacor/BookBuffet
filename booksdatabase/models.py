"""
This module contains the models for the Book Buffet application.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Book(models.Model):
    """
    A model representing a book.
    """
    title = models.CharField(max_length=255)
    subtitle = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField("Author", related_name="books_authored")
    publisher = models.CharField(max_length=255, null=True, blank=True)
    published_date = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    categories = models.ManyToManyField("Category", related_name="books_in_category")
    language = models.CharField(max_length=10, null=True, blank=True)
    preview_link = models.URLField(null=True, blank=True)
    cover = models.ImageField(upload_to="covers", null=True, blank=True)
    isbn_10 = models.CharField(max_length=10, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, null=True, blank=True)

    # ini buat nunjukkin review
    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.header}: {self.average_rating()}"


class Author(models.Model):
    """
    A model representing an author.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    """
    A model representing a category.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.header}: {self.rating}"
