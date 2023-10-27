from django.urls import path
from forum.views import *
from django.conf.urls.static import static
from django.conf import settings
from MyBooks.views import *

app_name = 'MyBooks'

urlpatterns = [
    path('', show_my_books, name='show_my_books'),
    path('rate/<int:post_id>/<int:rating>/', rate),
    path('create-product-ajax/<int:book_id>/', add_my_books, name='add_my_books')
]