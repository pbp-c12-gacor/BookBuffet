from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, AuthorViewSet, CategoryViewSet, BookList, BooksByCategory, BooksByAuthor, BooksByISBN, BooksByAuthorAndCategory, RatingsViewSet, RatingsByBook

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)
router.register("categories", CategoryViewSet)
router.register("ratings", RatingsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("search/", BookList.as_view()),
    path("authors/<int:author_id>/books", BooksByAuthor.as_view()),
    path("categories/<int:category_id>/books", BooksByCategory.as_view()),
    path("books/isbn/<str:isbn>", BooksByISBN.as_view()),
    path("authors/<int:author_id>/categories/<int:category_id>/books", BooksByAuthorAndCategory.as_view()),
    path("books/<int:book_id>/ratings", RatingsByBook.as_view()),
]
