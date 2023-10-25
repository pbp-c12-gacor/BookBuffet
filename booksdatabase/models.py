"""
This module contains the models for the Book Buffet application.
"""

from django.db import models


class Book(models.Model):
    """
    A model representing a book.
    """
    title = models.CharField(max_length=255)
    subtitle = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField("Author", related_name="books_authored")
    publisher = models.CharField(max_length=255)
    published_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    page_count = models.IntegerField()
    categories = models.ManyToManyField("Category", related_name="books_in_category")
    language = models.CharField(max_length=255)
    preview_link = models.URLField()
    cover = models.ImageField(upload_to="covers", null=True, blank=True)
    industry_identifiers = models.JSONField()


class Author(models.Model):
    """
    A model representing an author.
    """
    name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="authors_books")


class Category(models.Model):
    """
    A model representing a category.
    """
    name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="categories_books")
