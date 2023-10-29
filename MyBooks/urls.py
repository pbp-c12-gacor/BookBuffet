from django.urls import path
from forum.views import *
from django.conf.urls.static import static
from django.conf import settings
from MyBooks.views import *

app_name = 'MyBooks'

urlpatterns = [
    path('', show_my_books, name='show_my_books'),
    path('create-product-ajax/<int:book_id>/', add_my_books, name='add_my_books'),
    path('get-mybooks/', get_mybooks_json, name='get_mybooks_json'),
    path('add-review-ajax/<int:book_id>/', add_review, name ='add_review'),
    path('delete-mybooks/', remove_from_cart, name='remove_from_cart'),
    path('show-review/<int:book_id>', show_review, name ='show_review'),
    path('show-review/get-reviews/<int:book_id>', get_bookreviews_json, name='get_bookreviews_json'),
    path('show-review/get-user-reviews/<int:book_id>', get_user_review, name='get_user_review'),
    path('show-review/delete-review/<int:book_id>/', delete_review, name="delete_review")
]
