# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from booksdatabase.models import Book
from report.models import Report
from report.forms import ReportForm

# Fungsi untuk membuat laporan
# def create_report(request):
#     if request.method == 'POST':
#         form = ReportForm(request.POST)
#         if form.is_valid():
#             form.save()
            
#             previous_url = request.session.get('previous_url', '/')
            
#             # Bersihkan session
#             if 'previous_url' in request.session:
#                 del request.session['previous_url']
            
#             return redirect(previous_url)
#     else:
#         form = ReportForm()
    
#     return render(request, 'create_report.html', {'form': form})

# def create_report(request):
#     if request.method == 'POST':
#         form = ReportForm(request.POST)
#         if form.is_valid():
#             print("Udah valid")
#         form.user = request.user
#         book_title = request.POST.get('book', None)
#         form.book = Book.objects.get(title=book_title).id
#         form.comment = request.POST.get('comment')
#         print("belum valid")
#         print(request.POST)
#         print(form)
#         if form.is_valid():
#             print("dah valid")
#             # Cek apakah buku ada dalam data POST
#             book_title = request.POST.get('book', None)

#             # Jika buku tidak ada dalam data POST, cari buku berdasarkan judul yang dipilih
#             if book_title:
#                 try:
#                     book = Book.objects.get(title=book_title)
#                 except Book.DoesNotExist:
#                     book = None
#             else:
#                 book = None

#             comment = form.cleaned_data['comment']
#             # Simpan komentar dan buku yang sesuai dalam database
#             report = Report.objects.create(book=book, comment=comment)
#             return redirect('main:show_main')

#     else:
#         form = ReportForm()

#     return render(request, 'create_report.html', {'form': form})

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

def search_books(request):
    title = request.GET.get('search', '')

    if title:
        books = Book.objects.filter(title__icontains=title)
        book_list = [{'title': book.title} for book in books]

        return JsonResponse(book_list, safe=False)  # Tambahkan safe=False
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

# Fungsi hapus report untuk admin saja
def delete_report(request):
    user = request.user
    reports = Report.objects.all()