import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.urls import reverse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from booksdatabase.models import Book, Category, Author
from MyBooks.models import MyBook, Review
from .forms import NewUserForm

# Create your views here.
def show_main(request):
    # Get 2 books with the highest average rating
    all_books = Book.objects.all()
    for book in all_books:
        reviews = Review.objects.filter(book=book)
        if len(reviews) == 0:
            book.average_rating = 0
        else:
            book.average_rating = sum([review.rating for review in reviews]) / len(reviews)
    all_books = sorted(all_books, key=lambda book: book.average_rating, reverse=True)
    top_books = all_books[:3]
    
    # Get 4 books randomly
    random_picks = Book.objects.order_by('?')[:8]
    
    context = {
        'top_books': top_books,
        'random_picks': random_picks,
    }

    return render(request, "main.html", context)

def register(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['isAdmin'] == "True":
                referral_code = form.cleaned_data['referral_code']
                if referral_code != "PBPC12GACORMAXWIN":
                    messages.error(request, 'Invalid referral code for Admin registration.')
                    return redirect('main:register')
                user = form.save(commit=False)
                user.is_staff = True
                user.save()
            else:
                user = form.save(commit=False)
                user.is_staff = False
                user.save()
            messages.success(request, 'Your account has been successfully registered!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response