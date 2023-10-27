"""
Serializers for the booksdatabase app.
"""
from rest_framework import serializers
from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    """
    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    """
    # authors = serializers.StringRelatedField(many=True) # For debugging
    # categories = serializers.StringRelatedField(many=True) # For debugging
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        cover_data = validated_data.pop("cover", None)
        authors_data = validated_data.pop("authors")
        categories_data = validated_data.pop("categories")
        book = Book.objects.create(**validated_data)
        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(**author_data)
            book.authors.add(author)
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            book.categories.add(category)
        if cover_data is not None:
            ext = cover_data.name.split(".")[-1]
            book.cover.save(f"{book.id}.{ext}", cover_data, save=True)
        return book

    def update(self, instance, validated_data):
        cover_data = validated_data.pop("cover", None)
        authors_data = validated_data.pop("authors", None)
        categories_data = validated_data.pop("categories", None)
        book = super().update(instance, validated_data)
        if authors_data is not None:
            book.authors.clear()
            for author_data in authors_data:
                author, _ = Author.objects.get_or_create(**author_data)
                book.authors.add(author)
        if categories_data is not None:
            book.categories.clear()
            for category_data in categories_data:
                category, _ = Category.objects.get_or_create(**category_data)
                book.categories.add(category)
        # Cover image is not updated if cover_data is None (i.e. no new cover image is uploaded)
        if cover_data is not None and cover_data != instance.cover:
            instance.cover.delete()
            ext = cover_data.name.split(".")[-1]
            book.cover.save(f"{book.id}.{ext}", cover_data, save=True)
        return book
