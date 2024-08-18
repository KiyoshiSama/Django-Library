from django.db import models
from accounts.models import User
from books.models import Book

class ReturnedBook(models.Model):
    start_time = models.DateField()
    end_time = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"ReturnedBook: {self.book.title} - {self.customer.email}"