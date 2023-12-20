from django import forms
from django.forms import ModelForm
from .models import Publish

class PublishForm(ModelForm):
    class Meta:
        model = Publish
        fields = [
            'title', 'subtitle', 'authors', 'publisher', 'published_date', 
            'description', 'page_count', 'categories', 'language', 'preview_link', 
            'cover', 'isbn_10', 'isbn_13',
        ]

    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Type Your Title Here', 'class': 'custom-width'}),
        required=True
    )

    subtitle = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Subtitle', 'class': 'custom-width'}),
        required=False
    )

    authors = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Separate Each Authors with Comma', 'class': 'custom-width'}),
        required=False
    )

    publisher = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Publisher', 'class': 'custom-width'}),
        required=True
    )

    published_date = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'custom-width'}),
        required=False
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'custom-width'}),
        required=False
    )

    page_count = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'custom-width'}),
        required=False
    )

    categories = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Separate Each Categories with Comma', 'class': 'custom-width'}),
        required=True
    )

    language = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Language', 'class': 'custom-width'}),
        required=False
    )

    preview_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Preview Link', 'class': 'custom-width'}),
        required=False
    )

    cover = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/*', 'class': 'custom-width'}),
        required=False,
    )

    isbn_10 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'ISBN-10', 'class': 'custom-width'}),
        required=False,
        label="ISBN 10"
    )

    isbn_13 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'ISBN-13', 'class': 'custom-width'}),
        required=False,
        label="ISBN 13"
    )
