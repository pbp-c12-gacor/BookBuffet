import datetime
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from publish.models import Publish
from booksdatabase.models import Book
from django.contrib import messages 
from django.contrib.auth import logout
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_publish(request):
    context = {

    }
    return render(request, 'publish_book.html', context)

