from django.db import models
from accounts.models import User
from books.models import Book


class Hold(models.Model):
    start_time = models.DateField(blank=False)
    end_time = models.DateField(blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    create_date = models.DateTimeField(auto_now=True)

    ordering = ["create_date"]

    def __str__(self):
        return f"Hold: {self.book.title} - {self.customer.email}"
