from django import forms
from MyBooks.models import *


class MyBookForm(forms.ModelForm):
    class Meta:
        model = MyBook
        fields = ["books"]  

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review','rating']