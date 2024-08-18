import pytest
from rest_framework import status
from faker import Faker
from django.urls import reverse
from books.models import Author, Book, Publisher, Category

faker = Faker()


@pytest.mark.django_db
def test_author_list_url(authenticated_client):
    url = reverse("books-api:authors-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_author_detail_url(authenticated_client, authors):
    author = authors[0]
    url = reverse("books-api:authors-detail", args=[author.id])
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_author_url(authenticated_client):
    url = reverse("books-api:authors-list")
    data = {
        "name": faker.name(),
        "books": [],
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Author.objects.count() == 1
    assert Author.objects.get().name == data["name"]


@pytest.mark.django_db
def test_update_author_url(authenticated_client, authors):
    author = authors[0]
    url = reverse("books-api:authors-detail", args=[author.id])
    data = {
        "name": faker.name(),
        "books": [],
    }
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    author.refresh_from_db()
    assert author.name == data["name"]


@pytest.mark.django_db
def test_delete_author_url(authenticated_client, authors):
    author = authors[0]
    url = reverse("books-api:authors-detail", args=[author.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Author.objects.count() == len(authors) - 1


@pytest.mark.django_db
def test_book_list_url(authenticated_client):
    url = reverse("books-api:books-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_book_detail_url(authenticated_client, book):
    url = reverse("books-api:books-detail", args=[book.id])
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_book_url(authenticated_client, faker, authors, publisher, category):
    url = reverse("books-api:books-list")
    data = {
        "title": faker.word(),
        "description": faker.text(),
        "publisher": publisher.id,
        "category": category.id,
        "publish_date": faker.date(),
        "page_number": faker.random_number(),
        "is_available": faker.boolean(),
        "authors": [author.id for author in authors],
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.count() == 1
    created_book = Book.objects.get()
    assert created_book.title == data["title"]
    assert set(created_book.authors.values_list("id", flat=True)) == set(
        data["authors"]
    )


@pytest.mark.django_db
def test_update_book_url(authenticated_client, faker, book):
    url = reverse("books-api:books-detail", args=[book.id])
    data = {
        "title": faker.word(),
        "description": faker.text(),
        "publisher": book.publisher.id,
        "category": book.category.id,
        "publish_date": faker.date(),
        "page_number": faker.random_number(),
        "is_available": faker.boolean(),
        "authors": [author.id for author in book.authors.all()],
    }
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    book.refresh_from_db()
    assert book.title == data["title"]
    assert set(book.authors.values_list("id", flat=True)) == set(data["authors"])


@pytest.mark.django_db
def test_delete_book_url(authenticated_client, book):
    url = reverse("books-api:books-detail", args=[book.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_category_list_url(authenticated_client):
    url = reverse("books-api:categories-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_category_detail_url(authenticated_client, category):
    url = reverse("books-api:categories-detail", args=[category.id])
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_category_url(authenticated_client, faker):
    url = reverse("books-api:categories-list")
    data = {"name": faker.word()}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.count() == 1
    assert Category.objects.get().name == data["name"]


@pytest.mark.django_db
def test_update_category_url(authenticated_client, category, faker):
    url = reverse("books-api:categories-detail", args=[category.id])
    data = {"name": faker.word()}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    category.refresh_from_db()
    assert category.name == data["name"]


@pytest.mark.django_db
def test_delete_category_url(authenticated_client, category):
    url = reverse("books-api:categories-detail", args=[category.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_publisher_list_url(authenticated_client):
    url = reverse("books-api:publishers-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_publisher_detail_url(authenticated_client, publisher):
    url = reverse("books-api:publishers-detail", args=[publisher.id])
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_publisher_url(authenticated_client, faker):
    url = reverse("books-api:publishers-list")
    data = {"name": faker.company(), "address": faker.address()}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Publisher.objects.count() == 1
    assert Publisher.objects.get().name == data["name"]


@pytest.mark.django_db
def test_update_publisher_url(authenticated_client, publisher, faker):
    url = reverse("books-api:publishers-detail", args=[publisher.id])
    data = {"name": faker.company(), "address": faker.address()}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    publisher.refresh_from_db()
    assert publisher.name == data["name"]


@pytest.mark.django_db
def test_delete_publisher_url(authenticated_client, publisher):
    url = reverse("books-api:publishers-detail", args=[publisher.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Publisher.objects.count() == 0
