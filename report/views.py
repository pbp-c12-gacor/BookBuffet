# Create your views here.
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import serializers
import books_api
from booksdatabase.models import Book
from report.models import Report
from report.forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Fungsi untuk membuat laporan
@csrf_exempt
@login_required(login_url='/login')
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            book_title = form.cleaned_data.get('book_title')
            book = Book.objects.get(title=book_title)
            form.book = book #Ngambil objek berinstance 'Book'
            report = form.save(commit=False)
            report.user = request.user #Masukin User nya
            report.book_id = book.id #Masukin ID Book nya ke report ini
            report.save()
            return redirect('main:show_main')
    else:
        form = ReportForm()

    return render(request, 'create_report.html', {'form': form})

@csrf_exempt
@login_required(login_url='/login')
def create_report_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        new_report = Report.objects.create(
            book = Book.objects.get(title=data['book_title']),
            book_title = data['book_title'],
            user = request.user,
            comment = data["comment"],
        )

        new_report.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

def search_books(request):
    title = request.GET.get('search', '')

    if title:
        books = Book.objects.filter(title__icontains=title)
        book_list = [{'title': book.title} for book in books]

        return JsonResponse(book_list, safe=False)
    else:
        return JsonResponse([])  # Mengembalikan array kosong jika tidak ada hasil

# Fungsi tampilan report untuk admin saja
def show_report(request):
    user = request.user
    reports = Report.objects.all()
    if user.is_staff:
        reports = Report.objects.all()
        context = {
        'reports' : reports
    }
    context = {
        'reports' : reports
    }
    return render(request, "show_report.html", context)

# Fungsi untuk menampilkan semua report dalam JSON
def show_report_json(request):
    data = Report.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Fungsi hapus report untuk admin saja
def delete_report(request, id):
    report = Report.objects.get(pk = id)
    report.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"status": "success"})
    else:
        return HttpResponseRedirect(reverse('report:show_report'))
    
@csrf_exempt
def delete_report_flutter(request, id):
    report = Report.objects.get(pk = id)
    report.delete()
    return JsonResponse({"status": "success"}, status=200)
    
def get_user_by_id(request, user_id):
    user = User.objects.filter(id=user_id)
    return HttpResponse(serializers.serialize("json", user), content_type="application/json")