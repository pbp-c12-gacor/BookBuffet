from django.shortcuts import render
from django.contrib.auth import authenticate, login


# Create your views here.
def show_main(request):
    context = {
    }

    return render(request, "main.html", context)

