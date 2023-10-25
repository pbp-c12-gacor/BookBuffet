from rest_framework import serializers
from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        authors_data = validated_data.pop("authors")
        categories_data = validated_data.pop("categories")
        book = Book.objects.create(**validated_data)
        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(**author_data)
            book.authors.add(author)
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            book.categories.add(category)
        return book

    def update(self, instance, validated_data):
        authors_data = validated_data.pop("authors")
        categories_data = validated_data.pop("categories")
        instance.title = validated_data.get("title", instance.title)
        instance.subtitle = validated_data.get("subtitle", instance.subtitle)
        instance.publisher = validated_data.get("publisher", instance.publisher)
        instance.published_date = validated_data.get(
            "published_date", instance.published_date
        )
        instance.description = validated_data.get("description", instance.description)
        instance.page_count = validated_data.get("page_count", instance.page_count)
        instance.language = validated_data.get("language", instance.language)
        instance.preview_link = validated_data.get(
            "preview_link", instance.preview_link
        )
        instance.cover_link = validated_data.get("cover_link", instance.cover_link)
        instance.industry_identifiers = validated_data.get(
            "industry_identifiers", instance.industry_identifiers
        )
        instance.save()
        instance.authors.clear()
        instance.categories.clear()
        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(**author_data)
            instance.authors.add(author)
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.categories.add(category)
        return instance

    def delete(self, instance):
        instance.delete()
        return instance
