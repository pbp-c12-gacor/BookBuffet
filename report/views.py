# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from booksdatabase.models import Book
from report.models import Report
from report.forms import ReportForm

# Fungsi untuk membuat laporan
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            
            previous_url = request.session.get('previous_url', '/')
            
            # Bersihkan session
            if 'previous_url' in request.session:
                del request.session['previous_url']
            
            return redirect(previous_url)
    else:
        form = ReportForm()
    
    return render(request, 'create_report.html', {'form': form})

# Fungsi API untuk memberikan saran judul buku
def get_book_suggestions(request):
    query = request.GET.get('term', '')
    books = Book.objects.filter(title__icontains=query)
    suggestions = list(books.values_list('title', flat=True))
    return JsonResponse(suggestions, safe=False)
