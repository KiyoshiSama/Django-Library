from django.contrib import admin
from transactions.models import Checkout, Hold


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "book", "customer", "is_returned")
    search_fields = ("book__title", "customer__email")
    list_filter = ("book", "customer", "is_returned")


class HoldAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "book", "customer", "create_date")
    search_fields = ("book__title", "customer__email")
    list_filter = ("book", "customer")


admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Hold, HoldAdmin)