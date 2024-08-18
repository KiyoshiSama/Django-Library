import pytest
from faker import Faker
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.cache import cache
from books.models import Author, Book, Publisher, Category

User = get_user_model()

faker = Faker()


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()

@pytest.fixture
def user(db):
    user = User.objects.create_user(
        email=faker.email(),
        password=faker.password(),
    )
    return user


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def authors():
    return [Author.objects.create(name=faker.name()) for _ in range(3)]


@pytest.fixture
def publisher():
    return Publisher.objects.create(name=faker.company(), address=faker.address())


@pytest.fixture
def category():
    return Category.objects.create(name=faker.word())


@pytest.fixture
def book(authors, publisher, category):
    book = Book.objects.create(
        title=faker.word(),
        description=faker.text(),
        publisher=publisher,
        category=category,
        publish_date=faker.date(),
        page_number=faker.random_number(),
        is_available=faker.boolean(),
    )
    book.authors.set(authors)
    return book


