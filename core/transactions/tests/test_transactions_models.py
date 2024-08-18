import pytest
from datetime import timedelta
from django.utils import timezone
from transactions.models import Checkout, Hold


@pytest.mark.django_db
def test_checkout_creation(checkout):
    assert Checkout.objects.count() == 1
    assert checkout.start_time == timezone.now().date()
    assert checkout.end_time == (timezone.now() + timedelta(days=14)).date()
    assert checkout.book is not None
    assert checkout.customer is not None
    assert checkout.is_returned is False


@pytest.mark.django_db
def test_checkout_str_method(checkout):
    expected_str = f"Checkout: {checkout.book.title} - {checkout.customer.email}"
    assert str(checkout) == expected_str


@pytest.mark.django_db
def test_checkout_update(checkout):
    checkout.is_returned = True
    checkout.save()
    updated_checkout = Checkout.objects.get(id=checkout.id)
    assert updated_checkout.is_returned is True


@pytest.mark.django_db
def test_hold_creation(hold):
    assert Hold.objects.count() == 1
    assert hold.start_time == timezone.now().date()
    assert hold.end_time == (timezone.now() + timedelta(days=14)).date()
    assert hold.book is not None
    assert hold.customer is not None


@pytest.mark.django_db
def test_hold_str_method(hold):
    expected_str = f"Hold: {hold.book.title} - {hold.customer.email}"
    assert str(hold) == expected_str


@pytest.mark.django_db
def test_hold_update(hold):
    old_create_date = hold.create_date
    hold.save()
    updated_hold = Hold.objects.get(id=hold.id)
    assert updated_hold.create_date != old_create_date


@pytest.mark.django_db
def test_checkout_book_availability(book, user):

    assert book.is_available is True

    checkout = Checkout.objects.create(
        start_time=timezone.now().date(),
        end_time=(timezone.now() + timedelta(days=14)).date(),
        book=book,
        customer=user,
        is_returned=False,
    )
    assert book.is_available is False
    checkout.is_returned = True
    checkout.save()
    book.refresh_from_db()
    assert book.is_available is True


@pytest.mark.django_db
def test_hold_and_checkout_relationship(checkout, hold):
    assert Checkout.objects.count() == 1
    assert Hold.objects.count() == 1
    assert checkout.book == hold.book
    assert checkout.customer == hold.customer
