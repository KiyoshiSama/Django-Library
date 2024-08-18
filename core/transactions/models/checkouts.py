from django.db import models
from accounts.models import User
from books.models import Book


class Checkout(models.Model):
    start_time = models.DateField(blank=False)
    end_time = models.DateField(blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Checkout: {self.book.title} - {self.customer.email}"
