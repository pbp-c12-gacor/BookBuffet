from django.shortcuts import render
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
# Create your views here.
# def show_my_books(request):
#     return render(request, 'mybooks.html')

Review.objects.all().delete()

def show_my_books(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    # for post in books:
    #     rating = Rating.objects.filter(books=books, user=request.user).first()
    #     post.user_rating = rating.rating if rating else 0
    return render(request, "mybooks.html", {"posts": books})



@csrf_exempt
def add_my_books(request: HttpRequest, book_id:int):
    book = Book.objects.get(id= book_id)
    print("tes1")
    my_book, created = MyBook.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        my_book.books.add(book)
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()


@login_required(login_url='/login')
def get_mybooks_json(request):
    my_book, created = MyBook.objects.get_or_create(user=request.user)
    return HttpResponse(serializers.serialize('json', my_book.books.all()))

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'DELETE':
        book_id = json.loads(request.body).get('id')
        user = request.user
        my_book, created = MyBook.objects.get_or_create(user=user)
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
        print(rating)
        print(review)
        user = request.user
        book = Book.objects.get(pk = book_id)

        new_review = Review(rating=rating, review=review, user=user, book=book)
        new_review.save()
        print("tes faza 2")

        return HttpResponse(b"CREATED", 201)
    return HttpResponseNotFound()
    

@csrf_exempt
def show_review(request, book_id):
    book = Book.objects.get(id = book_id)
    review = Review.objects.filter(book=book)
    average_rating = Review.objects.filter(book = book).aggregate(Avg("rating"))["rating__avg"] or 0
    context = {
        'book':book,
        'reviews': review,
        'average': average_rating
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

def edit_review(request, book_id, reviewId):
    review = Review.objects.get(pk = reviewId)
    form = ReviewForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse("reviewbook:show_review"))
    
    context = {'form': form}
    return render(request, "review.html", context)

