from django.forms import ModelForm
from .models import Publish

class PublishForm(ModelForm):
    class Meta:
        model = Publish
        fields = ['title', 'subtitle', 'authors', 'publisher', 'published_date', 
                'description', 'page_count', 'categories', 'language', 'preview_link', 
                'cover', 'isbn_10', 'isbn_13'
                ]