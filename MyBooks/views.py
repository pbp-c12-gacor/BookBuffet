from django.shortcuts import render
from booksdatabase.models import *
# Create your views here.

def show_my_books(request):
    return render(request, 'mybooks.html')