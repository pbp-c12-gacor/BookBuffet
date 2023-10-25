from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField("Author", related_name="books")
    publisher = models.CharField(max_length=255)
    published_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    page_count = models.IntegerField()
    categories = models.ManyToManyField("Category", related_name="books")
    language = models.CharField(max_length=255)
    preview_link = models.URLField()
    cover_link = models.URLField(null=True, blank=True)
    industry_identifiers = models.JSONField()


class Author(models.Model):
    name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="authors")


class Category(models.Model):
    name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="categories")
