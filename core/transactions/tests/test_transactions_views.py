import pytest
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone


@pytest.mark.django_db
def test_borrow_book(authenticated_client, book):
    # Ensure the book is available before testing
    book.is_available = True
    book.save()

    url = reverse("borrow-book")
    data = {
        "start_time": timezone.now().date(),
        "end_time": (timezone.now() + timedelta(days=14)).date(),
        "book": book.id,
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["detail"] == "book successfully borrowed"
    book.refresh_from_db()
    assert not book.is_available


@pytest.mark.django_db
def test_borrow_book_already_reserved(authenticated_client, book, checkout):
    book.is_available = False
    book.save()

    url = reverse("borrow-book")
    data = {
        "start_time": timezone.now().date(),
        "end_time": (timezone.now() + timedelta(days=14)).date(),
        "book": book.id,
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == 200
    assert response.data["detail"] == "you've already reserved this book"


@pytest.mark.django_db
def test_borrow_book_invalid_data(authenticated_client, book):
    book.is_available = True
    book.save()

    url = reverse("borrow-book")
    data = {"start_time": timezone.now().date(), "end_time": "", "book": ""}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "end_time" in response.data


@pytest.mark.django_db
def test_borrow_book_unauthenticated(client, book):
    book.is_available = True
    book.save()

    url = reverse("borrow-book")
    data = {
        "start_time": timezone.now().date(),
        "end_time": (timezone.now() + timedelta(days=14)).date(),
        "book": book.id,
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_borrowed_books(authenticated_client, checkout):
    url = reverse("borrowed-list")
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == checkout.id


@pytest.mark.django_db
def test_update_borrowed_book(authenticated_client, checkout):
    url = reverse("borrowed-book", kwargs={"pk": checkout.id})
    data = {"is_returned": True}
    response = authenticated_client.patch(url, data, format="json")
    assert response.status_code == 200
    checkout.refresh_from_db()
    assert checkout.is_returned


@pytest.mark.django_db
def test_update_borrowed_book_unauthorized(client, checkout):
    url = reverse("borrowed-book", kwargs={"pk": checkout.id})
    data = {"is_returned": True}
    response = client.patch(url, data, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_hold_list_books(authenticated_client, hold):
    url = reverse("hold-list")
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == hold.id


@pytest.mark.django_db
def test_user_hold_list_books_unauthorized(client, hold):
    url = reverse("hold-list")
    response = client.get(url)
    assert response.status_code == 401
