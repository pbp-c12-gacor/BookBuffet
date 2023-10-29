from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.show_catalog, name="show_catalog"),
    path("books/<int:book_id>/", views.show_book, name="show_book"),
]