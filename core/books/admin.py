import csv
from django.contrib import admin
from django.http import HttpResponse
from books.models import Author, Book, Publisher, Category
from transactions.models import ReturnedBook


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "updated")
    search_fields = ("name",)


class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "publisher",
        "category",
        "publish_date",
        "is_available",
        "created",
        "updated",
    )
    search_fields = ("title",)
    list_filter = ("publisher", "category", "is_available")
    filter_horizontal = ("authors",)
    actions = ["get_report"]

    @admin.action(description="Get report of the selected books")
    def get_report(self, request, queryset):
        selected_books = queryset.values_list("title", flat=True)
        returned_books = ReturnedBook.objects.filter(book__title__in=selected_books)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="report.csv"'
        writer = csv.writer(response)
        writer.writerow(["Customer_ID","Start_Time", "End_Time", "Book_Title"])
        for returned_book in returned_books:
            writer.writerow(
                [
                    returned_book.customer.id,
                    returned_book.start_time,
                    returned_book.end_time,
                    returned_book.book.title,
                ]
            )

        return response

    get_report.short_description = "Generate Report for Selected Books"


class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "created", "updated")
    search_fields = ("name",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "updated")
    search_fields = ("name",)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Category, CategoryAdmin)
