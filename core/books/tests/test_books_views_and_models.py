import pytest
from rest_framework import status
from django.urls import reverse
from books.models import Author, Book, Publisher, Category


@pytest.mark.django_db
def test_create_author(authenticated_client, faker):
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
def test_list_authors(authenticated_client, authors):
    url = reverse("books-api:authors-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(authors)


@pytest.mark.django_db
def test_update_author(authenticated_client, faker, authors):
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
def test_delete_author(authenticated_client, authors):
    author = authors[0]
    url = reverse("books-api:authors-detail", args=[author.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Author.objects.count() == len(authors) - 1


@pytest.mark.django_db
def test_create_book(authenticated_client, faker, authors, publisher, category):
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
def test_list_books(authenticated_client, book):
    url = reverse("books-api:books-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_update_book(authenticated_client, faker, book):
    url = reverse("books-api:books-detail", args=[book.id])
    new_author = Author.objects.create(name=faker.name())
    data = {
        "title": faker.word(),
        "description": faker.text(),
        "publisher": book.publisher.id,
        "category": book.category.id,
        "publish_date": faker.date(),
        "page_number": faker.random_number(),
        "is_available": faker.boolean(),
        "authors": [author.id for author in [*book.authors.all(), new_author]],
    }
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    book.refresh_from_db()
    assert book.title == data["title"]
    assert set(book.authors.values_list("id", flat=True)) == set(data["authors"])


@pytest.mark.django_db
def test_delete_book(authenticated_client, book):
    url = reverse("books-api:books-detail", args=[book.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_create_category(authenticated_client, faker):
    url = reverse("books-api:categories-list")
    data = {"name": faker.word()}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.count() == 1
    assert Category.objects.get().name == data["name"]


@pytest.mark.django_db
def test_list_categories(authenticated_client, category):
    url = reverse("books-api:categories-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_update_category(authenticated_client, faker, category):
    url = reverse("books-api:categories-detail", args=[category.id])
    data = {"name": faker.word()}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    category.refresh_from_db()
    assert category.name == data["name"]


@pytest.mark.django_db
def test_delete_category(authenticated_client, category):
    url = reverse("books-api:categories-detail", args=[category.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_create_publisher(authenticated_client, faker):
    url = reverse("books-api:publishers-list")
    data = {"name": faker.company(), "address": faker.address()}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Publisher.objects.count() == 1
    assert Publisher.objects.get().name == data["name"]


@pytest.mark.django_db
def test_list_publishers(authenticated_client, publisher):
    url = reverse("books-api:publishers-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_update_publisher(authenticated_client, faker, publisher):
    url = reverse("books-api:publishers-detail", args=[publisher.id])
    data = {"name": faker.company(), "address": faker.address()}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    publisher.refresh_from_db()
    assert publisher.name == data["name"]


@pytest.mark.django_db
def test_delete_publisher(authenticated_client, publisher):
    url = reverse("books-api:publishers-detail", args=[publisher.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Publisher.objects.count() == 0


@pytest.mark.django_db
def test_create_author_with_invalid_data(authenticated_client):
    url = reverse("books-api:authors-list")
    data = {
        "books": [],
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data


@pytest.mark.django_db
def test_update_author_with_invalid_data(authenticated_client, authors):
    author = authors[0]
    url = reverse("books-api:authors-detail", args=[author.id])
    data = {
        "books": [],
    }
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data


@pytest.mark.django_db
def test_create_author_without_auth(api_client, faker):
    url = reverse("books-api:authors-list")
    data = {"name": faker.name(), "books": []}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_author_without_auth(api_client, authors, faker):
    author = authors[0]
    url = reverse("books-api:authors-detail", args=[author.id])
    data = {"name": faker.name(), "books": []}
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_author_without_auth(api_client, authors):
    author = authors[0]
    url = reverse("books-api:authors-detail", args=[author.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_book_with_invalid_data(
    authenticated_client, faker, authors, publisher, category
):
    url = reverse("books-api:books-list")
    data = {
        "title": "",
        "description": faker.text(),
        "publisher": publisher.id,
        "category": category.id,
        "publish_date": faker.date(),
        "page_number": faker.random_number(),
        "is_available": faker.boolean(),
        "authors": [author.id for author in authors],
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data


@pytest.mark.django_db
def test_update_book_with_invalid_data(authenticated_client, book, faker):
    url = reverse("books-api:books-detail", args=[book.id])
    data = {
        "description": faker.text(),
        "publisher": book.publisher.id,
        "category": book.category.id,
        "publish_date": faker.date(),
        "page_number": faker.random_number(),
        "is_available": faker.boolean(),
        "authors": [Author.objects.create(name=faker.name()).id],
    }
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data


@pytest.mark.django_db
def test_create_category_with_invalid_data(authenticated_client):
    url = reverse("books-api:categories-list")
    data = {}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data


@pytest.mark.django_db
def test_update_category_with_invalid_data(authenticated_client, category):
    url = reverse("books-api:categories-detail", args=[category.id])
    data = {}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data


@pytest.mark.django_db
def test_create_publisher_with_invalid_data(authenticated_client):
    url = reverse("books-api:publishers-list")
    data = {}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert "address" in response.data


@pytest.mark.django_db
def test_update_publisher_with_invalid_data(authenticated_client, publisher):
    url = reverse("books-api:publishers-detail", args=[publisher.id])
    data = {}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert "address" in response.data


@pytest.mark.django_db
def test_delete_book_without_auth(api_client, book):
    url = reverse("books-api:books-detail", args=[book.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_books_without_auth(api_client):
    url = reverse("books-api:books-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_categories_without_auth(api_client):
    url = reverse("books-api:categories-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_publishers_without_auth(api_client):
    url = reverse("books-api:publishers-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
