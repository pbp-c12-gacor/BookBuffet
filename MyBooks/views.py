from django.shortcuts import render
from booksdatabase.models import *
from MyBooks.models import *
from django.shortcuts import HttpResponse
from django.http import HttpRequest

# Create your views here.

# def show_my_books(request):
#     return render(request, 'mybooks.html')



def show_my_books(request: HttpRequest) -> HttpResponse:
    posts = MyBook.objects.all()
    for post in posts:
        rating = Rating.objects.filter(post=post.Book, user=request.user).first()
        post.user_rating = rating.rating if rating else 0
    return render(request, "mybooks.html", {"posts": posts})

def rate(request: HttpRequest, post_id: int, rating: int) -> HttpResponse:
    post = Book.objects.get(id=post_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating)
    return show_my_books(request)