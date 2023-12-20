from audioop import avg
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
from django.db.models import Avg

@login_required(login_url='/login')
def show_my_books(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    mybookForm = MyBookForm(request.POST or None)
    
    return render(request, "mybooks.html", {"posts": books, 'mybookForm' : mybookForm })



@csrf_exempt
def add_my_books(request: HttpRequest, book_id:int):
    book = Book.objects.get(id= book_id)
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
    #     return HttpResponse(b"DELETED", 201)

    # return HttpResponseNotFound()

@login_required
@csrf_exempt
def delete_mybook_flutter(request, book_id:int):
    # if request.method == "DELETE":
    my_book, created = MyBook.objects.get_or_create(user=request.user)
    try:
        review = Review.objects.filter(user= request.user).get(book = book_id)
        review.delete()
    except:
        review = None
    book = Book.objects.get(id =  book_id)
    my_book.books.remove(book)
    # return HttpResponse({'message': 'book deleted successfully'}, status=200)
    return JsonResponse({"status": "success"}, status=200)

    # return HttpResponseNotFound()


@csrf_exempt
def add_review(request:HttpRequest, book_id:int):
    if request.method == 'POST':
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        user = request.user
        book = Book.objects.get(pk = book_id)
        name = user.username
        new_review = Review(rating=rating, review=review, user=user, book=book, username = name)
        new_review.save()

        return HttpResponse(b"CREATED", 201)
    return HttpResponseNotFound()
    
@csrf_exempt
def add_review_flutter(request, book_id:int):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        new_review = Review(rating=data["rating"], review=data["review"], user=request.user, book=Book.objects.get(pk = book_id), username = request.user.username)
        new_review.save()
        # new_post = Post.objects.create(
        #     user = request.user,
        #     title = data["title"],
        #     text = data["text"],
        # )

        # new_post.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

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
# Review.objects.all().delete()

def get_bookreviews_json(request, book_id):
    book = Book.objects.get(pk = book_id)
    review = Review.objects.filter(book=book)
    return HttpResponse(serializers.serialize('json', review))


def get_user_review(request, book_id):
    book = Book.objects.get(pk = book_id)
    review = Review.objects.filter(user=request.user, book=book)
    return HttpResponse(serializers.serialize('json', review))


def get_user_review_flutter(request, book_id):
    book = Book.objects.get(pk = book_id)
    review = Review.objects.filter(user=request.user, book=book)
    return HttpResponse(serializers.serialize('json', review),content_type="application/json")  

@csrf_exempt
def delete_review(request, book_id):
    if request.method == 'DELETE':
        review = Review.objects.filter(user=request.user).get(book=book_id)
        review.delete()
        return HttpResponse(b"DELETED", status=200)
    return HttpResponseNotFound()


@csrf_exempt
def delete_review_flutter(request, book_id):

    review = Review.objects.filter(user=request.user.pk).get(book=book_id)
    review.delete()

    return JsonResponse({"status": "success"}, status=200)


@csrf_exempt
def add_mybooks_flutter(request, book_id):
    # data = json.loads(request.body)
    book = Book.objects.get(id= book_id)
    my_book, created = MyBook.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        my_book.books.add(book)

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)


@csrf_exempt
def add_review_flutter(request:HttpRequest, book_id:int):
    data = json.loads(request.body)

    if request.method == 'POST':
        rating = data["rating"]
        review = data["review"]
        user = request.user
        book = Book.objects.get(pk = book_id)
        name = user.username
        new_review = Review(rating=rating, review=review, user=user, book=book, username = name)
        new_review.save()

        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
@login_required
def show_post_json(request):
    my_book, created = MyBook.objects.get_or_create(user=request.user)
    return HttpResponse(serializers.serialize("json", my_book.books.all()), content_type="application/json")


def get_mybookmodel_json(request):
    my_book, created = MyBook.objects.get_or_create(user=request.user)
    return HttpResponse(('json', my_book))


def get_bookreviews_json_flutter(request, book_id):
    book = Book.objects.get(pk = book_id)
    review = Review.objects.filter(book=book)
    return HttpResponse(serializers.serialize('json', review), content_type="application/json")

def show_book(request, book_id):
    book = Book.objects.get(id=book_id)
    return HttpResponse(serializers.serialize('json', [book]), content_type="application/json")

def get_user_review_flutter(request, book_id):
    book = Book.objects.get(pk = book_id)
    review = Review.objects.filter(user=request.user, book=book)
    return HttpResponse(serializers.serialize('json', review),content_type="application/json")
# @csrf_exempt
# def show_comment(request):
#     data = Review.objects.all()
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")



# @csrf_exempt
# def get_my_books_flutter(request):
#     user = request.user
#     items = MyBook.objects.filter(user=user)
    
#     return JsonResponse(serializers.serialize('json', items), safe=False)



# @csrf_exempt
# def get_my_reviews_flutter(request):
#     user = request.user
#     items = MyBook.objects.filter(user=user)
    
#     return JsonResponse(serializers.serialize('json', items), safe=False)



# @csrf_exempt
# def create_post_flutter(request):
#     if request.method == 'POST':
        
#         data = json.loads(request.body)

#         new_post = Post.objects.create(
#             user = request.user,
#             title = data["title"],
#             text = data["text"],
#         )

#         new_post.save()

#         return JsonResponse({"status": "success"}, status=200)
#     else:
#         return JsonResponse({"status": "error"}, status=401)
    
# @csrf_exempt
# def create_comment_flutter(request):
#     if request.method == 'POST':
        
#         data = json.loads(request.body)
#         post = Post.objects.get(id=data['post_id'])
#         new_comment = Comment.objects.create(
#             user = request.user,
#             post = post,
#             text = data["text"],
#         )

#         new_comment.save()

#         return JsonResponse({"status": "success"}, status=200)
#     else:
#         return JsonResponse({"status": "error"}, status=401)
