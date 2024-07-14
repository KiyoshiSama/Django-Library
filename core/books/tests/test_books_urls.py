from django.test import SimpleTestCase
from django.urls import reverse, resolve
from books.api.views import AuthorsViewSet, BooksViewSet, CategoriesViewSet, PublishersViewSet

class TestUrls(SimpleTestCase):

    def test_authors_list_url_is_resolved(self):
        url = reverse('books-api:authors-list')
        self.assertEqual(resolve(url).func.cls, AuthorsViewSet)

    def test_authors_detail_url_is_resolved(self):
        url = reverse('books-api:authors-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, AuthorsViewSet)

    def test_books_list_url_is_resolved(self):
        url = reverse('books-api:books-list')
        self.assertEqual(resolve(url).func.cls, BooksViewSet)

    def test_books_detail_url_is_resolved(self):
        url = reverse('books-api:books-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, BooksViewSet)

    def test_categories_list_url_is_resolved(self):
        url = reverse('books-api:categories-list')
        self.assertEqual(resolve(url).func.cls, CategoriesViewSet)

    def test_categories_detail_url_is_resolved(self):
        url = reverse('books-api:categories-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, CategoriesViewSet)

    def test_publishers_list_url_is_resolved(self):
        url = reverse('books-api:publishers-list')
        self.assertEqual(resolve(url).func.cls, PublishersViewSet)

    def test_publishers_detail_url_is_resolved(self):
        url = reverse('books-api:publishers-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, PublishersViewSet)
