import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
def test_register_user(api_client, faker, user):
    url = reverse("accounts-api:create-account")
    email = faker.email()
    password = faker.password()
    data = {
        "email": email,
        "password": password,
        "password1": password,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == email


@pytest.mark.django_db
def test_register_user_password_mismatch(api_client, faker):
    url = reverse("accounts-api:create-account")
    data = {
        "email": faker.email(),
        "password": "TestPassword123",
        "password1": "DifferentPassword123",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_user_profile(authenticated_client, user):
    url = reverse("accounts-api:accounts")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_update_user_profile(authenticated_client, user):
    url = reverse("accounts-api:accounts")
    data = {"first_name": "Updated", "last_name": "Name"}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == "Updated"
    assert user.last_name == "Name"


@pytest.mark.django_db
def test_update_user_profile_invalid(authenticated_client, user):
    url = reverse("accounts-api:accounts")
    data = {"first_name": "", "last_name": ""}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_unauthorized_access(api_client):
    url = reverse("accounts-api:accounts")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
