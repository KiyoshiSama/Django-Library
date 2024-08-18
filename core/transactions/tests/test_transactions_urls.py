import pytest
from django.urls import reverse, resolve
from transactions.api.views import (
    BorrowBookGenericView,
    UserBorrowedBooksGenericView,
    UpdateBorrowedBookGenericView,
    UserHoldListBooksGenericView,
)


@pytest.mark.django_db
def test_borrow_book_url():
    url = reverse("borrow-book")
    assert resolve(url).func.view_class == BorrowBookGenericView


@pytest.mark.django_db
def test_borrowed_list_url():
    url = reverse("borrowed-list")
    assert resolve(url).func.view_class == UserBorrowedBooksGenericView


@pytest.mark.django_db
def test_borrowed_book_url():
    url = reverse("borrowed-book", kwargs={"pk": 1})
    assert resolve(url).func.view_class == UpdateBorrowedBookGenericView


@pytest.mark.django_db
def test_hold_list_url():
    url = reverse("hold-list")
    assert resolve(url).func.view_class == UserHoldListBooksGenericView
