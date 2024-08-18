from rest_framework import viewsets, filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from books.api.serializers import (
    AuthorSerializer,
    BookCreateUpdateSerializer,
    BookRetrieveSerializer,
    CategorySerializer,
    PublisherSerializer,
)
from books.models import Author, Book, Publisher, Category


class AuthorsViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BooksViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        "is_available",
    ]
    search_fields = [
        "name",
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookRetrieveSerializer
        return BookCreateUpdateSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PublishersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
