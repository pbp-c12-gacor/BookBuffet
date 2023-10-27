from django.forms import ModelForm
from MyBooks.models import *


class ProductForm(ModelForm):
    class Meta:
        model = MyBook
        fields = ["Book"]  