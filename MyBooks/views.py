from django.shortcuts import render
from booksdatabase.models import *
from MyBooks.models import *
from django.shortcuts import HttpResponse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# def show_my_books(request):
#     return render(request, 'mybooks.html')



def show_my_books(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    # for post in books:
    #     rating = Rating.objects.filter(books=books, user=request.user).first()
    #     post.user_rating = rating.rating if rating else 0
    return render(request, "mybooks.html", {"posts": books})

def rate(request: HttpRequest, post_id: int, rating: int) -> HttpResponse:
    post = Book.objects.get(id=post_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating)
    return show_my_books(request)

@csrf_exempt
def add_my_books(request: HttpRequest, book_id:int):
    book = Book.objects.get(id= book_id)
    print("tes1")
    if request.method == 'POST':
        user = request.user
        book_added = MyBook(Book = book, User=user)
        book_added.save()


        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()