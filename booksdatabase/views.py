from rest_framework import viewsets, filters, generics
from .models import Book, Author, Category
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer
from .permissions import IsAdminOrReadOnly


class PrefixSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get("search", None)
        if ":" in search:
            search_terms = search.split(",")
            for term in search_terms:
                if ":" not in term:
                    queryset = queryset.filter(title__icontains=term)
                prefix, value = term.split(":")
                value = value.strip()
                if prefix == "title":
                    queryset = queryset.filter(title__icontains=value)
                elif prefix == "author":
                    queryset = queryset.filter(authors__name__icontains=value)
                elif prefix == "category":
                    queryset = queryset.filter(categories__name__icontains=value)
        return queryset


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.cover.delete()
        return super().destroy(request, *args, **kwargs)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [PrefixSearchFilter]
    search_fields = ["title", "authors__name", "categories__name"]


class BooksByCategory(generics.ListAPIView):
    serializer_class = BookSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "category_id"

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Book.objects.filter(categories__pk=category_id)


class BooksByAuthor(generics.ListAPIView):
    serializer_class = BookSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "author_id"

    def get_queryset(self):
        author_id = self.kwargs["author_id"]
        return Book.objects.filter(authors__pk=author_id)


class BooksByISBN(generics.ListAPIView):
    serializer_class = BookSerializer
    lookup_field = "isbn"
    lookup_url_kwarg = "isbn"

    def get_queryset(self):
        isbn = self.kwargs["isbn"]
        return Book.objects.filter(isbn_13=isbn) | Book.objects.filter(isbn_10=isbn)


class BooksByAuthorAndCategory(generics.ListAPIView):
    serializer_class = BookSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "author_id"

    def get_queryset(self):
        author_id = self.kwargs["author_id"]
        category_id = self.kwargs["category_id"]
        return Book.objects.filter(authors__pk=author_id, categories__pk=category_id)