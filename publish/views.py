import datetime
import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from publish.models import Publish
from booksdatabase.models import Book, Author, Category
from django.contrib import messages 
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import PublishForm
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

@login_required(login_url='/login')
@csrf_exempt
# Method untuk melakukan pembuatan Publish
def publish_book(request):
    form = PublishForm()
    if request.method == 'POST':
        form = PublishForm(request.POST, request.FILES)
        if form.is_valid():
            new_publish = form.save(commit=False)
            new_publish.user = request.user
            new_publish.save()
    return render(request, 'publish_book.html', {'form': form})

def verify_publish(request):
    if request.user.is_staff:
        publish_to_verify = Publish.objects.filter(is_verified=False)
        return render(request, 'verify_publish.html', {'publish_to_verify': publish_to_verify})
    return render(request, 'not_permitted.html', {})

@login_required(login_url='/login')
def my_publish(request):
    publish = Publish.objects.filter(user = request.user)
    return render(request, 'my_publish.html', {'publish':publish})

def show_publish_detail(request, id):
    publish = Publish.objects.get(pk=id)
    context = {
        'title': publish.title,
        'authors': publish.authors,
        'publisher': publish.publisher,
        'published_date': publish.published_date if publish.published_date else "-",
        'description': publish.description if publish.description else "-",
        'page_count': publish.page_count if publish.page_count else "-",
        'categories': publish.categories,
        'language': publish.language if publish.language else "-",
        'cover': publish.cover.url if publish.cover else None,
        'isbn_10': publish.isbn_10 if publish.isbn_10 else "-",
        'isbn_13': publish.isbn_13 if publish.isbn_13 else "-",
        'submitted_by': publish.user.username,
        'date_added': publish.date_added.strftime('%Y-%m-%d'),
    }
    return render(request, 'verify_book.html', context)

@csrf_exempt
def confirming_publish(request, id):
    if request.method == 'POST':
        publish = Publish.objects.get(pk=id)
        verify = request.POST.get('verify')
        if verify == 'true':
            authors = publish.authors.split(',')
            categories = publish.categories.split(',')
            book_authors = []
            for author in authors:
                author, created = Author.objects.get_or_create(name=author)
                book_authors.append(author)
            book_categories = []
            for category in categories:
                category, created = Category.objects.get_or_create(name=category)
                book_categories.append(category)
            book = Book(
                title=publish.title,
                publisher=publish.publisher,
                published_date=publish.published_date,
                description=publish.description,
                page_count=publish.page_count,
                language=publish.language,
                cover=publish.cover,
                isbn_10=publish.isbn_10,
                isbn_13=publish.isbn_13
            )
            book.save()
            book.authors.set(book_authors)
            book.categories.set(book_categories)
            publish.is_verified = True
            publish.is_valid = True
            publish.save()
            return JsonResponse({'message': 'Book published successfully'})
        elif verify == 'false':
            publish.is_verified = True
            publish.save()
            return JsonResponse({'message': 'Book rejected successfully'})


def get_publish_by_id(request, publish_id):
    publish = Publish.objects.get(pk=publish_id)
    return HttpResponse(serializers.serialize("json", publish), content_type="application/json")

def get_unverified_publish(request):
    publish = Publish.objects.filter(is_verified=False)
    return HttpResponse(serializers.serialize("json", publish), content_type="application/json")

def get_publish(request):
    publish = Publish.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', publish), content_type="application/json")

def get_user(request, id):
    publish = Publish.objects.get(pk=id)
    username = publish.user.username
    data = {'username': username}
    return JsonResponse(data)

@csrf_exempt
def delete_publish_by_id(request, id):
    publish = Publish.objects.get(pk=id)
    publish.delete()
    return HttpResponse(b"DELETED", status=201)

@csrf_exempt
def delete_all_publish(request):
    try:
        # Delete all rows from the "publish" table
        Publish.objects.all().delete()
        return HttpResponse(b"DELETED", status=201)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
    
@csrf_exempt
def create_publish_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_publish = Publish.objects.create(
            user = request.user,
            title = data["title"],
            subtitle = data["subtitle"],
            authors = data["authors"],
            publisher = data["publisher"],
            published_date = data["published_date"],
            description = data["description"],
            page_count = data["page_count"],
            categories = data["categories"],
            language = data["language"],
            preview_link = data["preview_link"],
            cover = data["cover"],
            isbn_10 = data["isbn_10"],
            isbn_13 = data["isbn_13"],
        )

        new_publish.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def delete_publish_flutter(request):
    
    return