from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from booksdatabase.models import Book, Category, Author, Rating

# Create your views here.
def show_catalog(request):
    all_books = Book.objects.all()
    
    books_by_category = {}
    categories = Category.objects.all()
    for category in categories:
        books_by_category[category] = Book.objects.filter(categories=category)
    
    business = Category.objects.get(name='Business & Economics')
    business.processed_name = 'business-and-economics'
    
    biography = Category.objects.get(name='Biography & Autobiography')
    biography.processed_name = 'biography-and-autobiography'
    
    science = Category.objects.get(name='Science')
    science.processed_name = 'science'
    
    fiction = Category.objects.get(name='Fiction')
    fiction.processed_name = 'fiction'
    
    self_help = Category.objects.get(name='Self-Help')
    self_help.processed_name = 'self-help'
    
    popular_categories = {business, biography, science, fiction, self_help}
    
    categories = set(categories) - popular_categories
    for category in categories:
        category.processed_name = category.name.replace(' ', '-').replace('&', 'and').lower()
    
    context = {
        'popular_categories': popular_categories,
        'categories': categories,
        'all_books': all_books,
        'books_by_category': books_by_category,
    }
    for category in categories:
        print(f"{category}:")
        for book in books_by_category[category]:
            print(f"  {book.title}")
    return render(request, 'catalog.html', context)

def show_book(request, book_id):
    book = Book.objects.get(id=book_id)
    ratings = Rating.objects.filter(book=book)

    context = {
        'book': book,
        'ratings': ratings,
    }

    return render(request, 'book.html', context)

def show_books(request):
    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, 'books.html', context)
