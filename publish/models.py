from django.db import models
from django.contrib.auth.models import User
from booksdatabase.models import Author

# Create your models here.
class Publish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField("Author", related_name="books_authored")
    publisher = models.CharField(max_length=255, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    categories = models.ManyToManyField("Category", related_name="books_in_category")
    language = models.CharField(max_length=10, null=True, blank=True)
    preview_link = models.URLField(null=True, blank=True)
    cover = models.ImageField(upload_to="covers", null=True, blank=True)
    isbn_10 = models.CharField(max_length=10, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, null=True, blank=True)