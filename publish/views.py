import datetime
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from publish.models import Publish
from booksdatabase.models import Book
from django.contrib import messages 
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import PublishForm
from django.contrib.auth.decorators import user_passes_test

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
            # return HttpResponseRedirect(reverse('main:show_main'))
    return render(request, 'publish_book.html', {'form': form})

def verify_publish(request):
    if request.user.is_staff:
        publish_to_verify = Publish.objects.filter(is_verified=False)
        return render(request, 'verify_publish.html', {'publish_to_verify': publish_to_verify})
    return render(request, 'not_permitted.html', {})

def my_publish(request):
    publish = Publish.objects.filter(user = request.user)
    return render(request, 'my_publish.html', {'publish':publish})

def show_publish_detail(request, publish_id):
    publish = get_object_or_404(Publish, pk=publish_id)

    if request.method == 'POST':
        if request.POST.get('verify') == 'true':
            book = Book(
                title=publish.title,
                authors=publish.authors.all(),
                publisher=publish.publisher,
                published_date=publish.published_date,
                description=publish.description,
                page_count=publish.page_count,
                categories=publish.categories.all(),
                language=publish.language,
                cover=publish.cover,
                isbn_10=publish.isbn_10,
                isbn_13=publish.isbn_13
            )
            book.save()
            publish.is_verified = True
            publish.is_valid = True
            publish.save()
            return redirect('publish:verify_publish')
        elif request.POST.get('verify') == 'false':
            publish.is_verified = True
            publish.save()
            return redirect('publish:verify_publish')
    return render(request, 'verify_book.html', {'publish': publish})

def get_publish_by_id(request, publish_id):
    publish = Publish.objects.get(pk=publish_id)
    return HttpResponse(serializers.serialize("json", publish), content_type="application/json")

def get_publish(request):
    publish = Publish.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', publish))