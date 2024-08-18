from rest_framework import serializers
from books.models import Author, Book, Category, Publisher


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "books",
        ]


class BookCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "description",
            "publisher",
            "category",
            "publish_date",
            "page_number",
            "is_available",
            "authors",
        )


class BookRetrieveSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "description",
            "publisher",
            "category",
            "publish_date",
            "page_number",
            "is_available",
            "authors",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "address"]
