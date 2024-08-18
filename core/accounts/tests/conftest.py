import pytest
from faker import Faker
from rest_framework.test import APIClient
from accounts.models import User

faker = Faker()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        email=faker.email(),
        password=faker.password(),
        is_first_login=True,
    )
    return user


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user_data():
    return {
        "email": faker.email(),
        "password": faker.password(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
    }


@pytest.fixture
def create_user(user_data):
    return User.objects.create_user(**user_data)


@pytest.fixture
def create_superuser(user_data):
    return User.objects.create_superuser(**user_data)
