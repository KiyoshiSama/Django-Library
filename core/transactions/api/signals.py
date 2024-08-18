from django.dispatch import receiver
from django.db.models.signals import post_save
from transactions.models import Checkout, Hold, ReturnedBook


@receiver(post_save, sender=Checkout)
def update_book_availabilty(sender, instance, **kwargs):
    book = instance.book
    if not instance.is_returned:
        book.is_available = False
        book.save()

    if instance.is_returned:
        hold_book = Hold.objects.filter(book=instance.book).first()
        if hold_book:
            Checkout.objects.create(
                start_time=hold_book.start_time,
                end_time=hold_book.end_time,
                book=hold_book.book,
                customer=hold_book.customer,
                is_returned=False,
            )
            hold_book.delete()
        else:
            # changing the book availablity to true if no one is on the hold list
            book.is_available = True
            book.save()

@receiver(post_save, sender=Checkout)
def create_returned_books(sender, instance, **kwargs):
    if instance.is_returned:
        ReturnedBook.objects.get_or_create(
            start_time=instance.start_time,
            end_time=instance.end_time,
            book=instance.book,
            customer=instance.customer,
        )
