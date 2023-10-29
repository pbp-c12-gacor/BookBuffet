from django.shortcuts import get_object_or_404, render
from booksdatabase.models import *
from MyBooks.models import *
from django.shortcuts import HttpResponse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from MyBooks.forms import *
import json


@login_required(login_url='/login')
def show_my_books(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    mybookForm = MyBookForm(request.POST or None)
    
    return render(request, "mybooks.html", {"posts": books, 'mybookForm' : mybookForm })



@csrf_exempt
def add_my_books(request: HttpRequest, book_id:int):
    book = Book.objects.get(id= book_id)
    print("tes1")
    my_book, created = MyBook.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        my_book.books.add(book)
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()


def get_mybooks_json(request):
    my_book, created = MyBook.objects.get_or_create(user=request.user)
    return HttpResponse(serializers.serialize('json', my_book.books.all()))

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'DELETE':
        book_id = json.loads(request.body).get('id')
        user = request.user
        my_book, created = MyBook.objects.get_or_create(user=user)

        try:
            review = Review.objects.filter(user= user).get(book = book_id)
            review.delete()
        except:
            review = None

        book = Book.objects.get(id= book_id)
        my_book.books.remove(book)
        return HttpResponse(b"DELETED", 201)

    return HttpResponseNotFound()




@csrf_exempt
def add_review(request:HttpRequest, book_id:int):
    print("masuk ga ya")
    if request.method == 'POST':
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        user = request.user
        book = Book.objects.get(pk = book_id)
        name = user.username
        new_review = Review(rating=rating, review=review, user=user, book=book, username = name)
        new_review.save()
        print("tes faza 2")

        return HttpResponse(b"CREATED", 201)
    return HttpResponseNotFound()
    

@login_required(login_url='/login')
@csrf_exempt
def show_review(request, book_id):  
    book = Book.objects.get(id = book_id)

    user = request.user
    try:
        mybook = MyBook.objects.filter(user=user).get(books=book)
    except:
        mybook = "kosong"

    review = Review.objects.filter(book=book)
    review_form= ReviewForm(request.POST or None)
    average_rating = Review.objects.filter(book = book).aggregate(Avg("rating"))["rating__avg"] or 0
    context = {
        'book':book,
        'reviews': review,
        'average': average_rating,
        'mybook' : mybook,
        'review_form' : review_form

    }

    return render(request, "review.html", context)


def get_bookreviews_json(request, book_id):
    print("masuk gaya")
    book = Book.objects.get(pk = book_id)
    review = Review.objects.filter(book=book)
    return HttpResponse(serializers.serialize('json', review))


def get_user_review(request, book_id):
    book = Book.objects.get(pk = book_id)
    review = Review.objects.filter(user=request.user, book=book)
    return HttpResponse(serializers.serialize('json', review))


@csrf_exempt
def delete_review(request, book_id):
    if request.method == 'DELETE':
        review = Review.objects.filter(user=request.user).get(book=book_id)
        review.delete()
        return HttpResponse(b"DELETED", status=200)
    return HttpResponseNotFound()
