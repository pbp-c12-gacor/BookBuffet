from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, AuthorViewSet, CategoryViewSet, BookList, BookDetail

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)
router.register("categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("search/", BookList.as_view()),
    path("book/<int:book_id>/", BookDetail.as_view()),
]
