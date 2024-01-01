import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from booksdatabase.models import Book, Category, Author
from MyBooks.models import MyBook, Review

# Create your views here.
def show_catalog(request):
    user = request.user
    show_logout = user.is_authenticated 
    all_books = Book.objects.all()
    for book in all_books:
        reviews = Review.objects.filter(book=book)
        if len(reviews) == 0:
            book.average_rating = 0
        else:
            book.average_rating = sum([review.rating for review in reviews]) / len(reviews)
    all_books = sorted(all_books, key=lambda book: book.average_rating, reverse=True)
    
    categories = Category.objects.all()
    for category in categories:
        category.processed_name = category.name.replace('&', 'and').replace(' ', '-').lower()
        books = Book.objects.filter(categories=category)
        for book in books:
            reviews = Review.objects.filter(book=book)
            if len(reviews) == 0:
                book.average_rating = 0
            else:
                book.average_rating = round(sum([review.rating for review in reviews]) / len(reviews),2)
        category.books = sorted(books, key=lambda book: book.average_rating, reverse=True)
    
    context = {
        'categories': categories,
        'all_books': all_books,
        'show_logout': show_logout
    }
    
    return render(request, 'catalog.html', context)

def show_book(request, book_id):
    user = request.user
    show_logout = user.is_authenticated 
    book = Book.objects.get(id=book_id)

    context = {
        'book': book,
        'show_logout': show_logout
    }

    return render(request, 'book.html', context)
