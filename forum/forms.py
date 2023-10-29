from django.forms import ModelForm
from booksdatabase.models import Book
from forum.models import Post, Comment
from django import forms

class PostForm(forms.ModelForm):
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control border-0 my-2', 'placeholder': 'Type Your Title Here', 'id': 'title'}))
    text = forms.CharField(label=False, widget=forms.Textarea(attrs={'class': 'form-control border-0 my-2', 'rows': 3, 'placeholder': "What's Happening?", 'id': 'description'}))
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=False, widget=forms.HiddenInput(attrs={'required': False, 'id': 'book-selected'}))
    class Meta:
        model = Post
        fields = ["title", "text", "book"]
class CommentForm(ModelForm):
    text = forms.CharField(label=False,widget=forms.Textarea(attrs={'class': 'form-control border-0','placeholder': 'Post your reply','id': 'content','name': 'content','rows': '3'}))
    class Meta:
        model = Comment 
        fields = ["text"]

class PostEditForm(forms.ModelForm):
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control border-0 my-2', 'placeholder': 'Type Your Title Here', 'id': 'title-edit'}))
    text = forms.CharField(label=False, widget=forms.Textarea(attrs={'class': 'form-control border-0 my-2', 'rows': 3, 'placeholder': "What's Happening?", 'id': 'description-edit'}))
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=False, widget=forms.HiddenInput(attrs={'required': False, 'id': 'book-selected-edit'}))
    class Meta:
        model = Post
        fields = ["title", "text", "book"]

class CommentEditForm(ModelForm):
    text = forms.CharField(label=False,widget=forms.Textarea(attrs={'class': 'form-control border-0','placeholder': 'Post your reply','id': 'content-edit','name': 'content','rows': '3'}))
    class Meta:
        model = Comment 
        fields = ["text"]