from django import forms
from MyBooks.models import *


# class ProductForm(ModelForm):
#     class Meta:
#         model = MyBook
#         fields = ["Book"]  

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review','rating']