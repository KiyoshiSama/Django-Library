from django.urls import path
from transactions.api import views

urlpatterns = [
    path("", views.BorrowBookGenericView.as_view(), name="borrow-book"),
    path(
        "borrowed-books/",
        views.UserBorrowedBooksGenericView.as_view(),
        name="borrowed-list",
    ),
    path(
        "borrowed-books/<int:pk>",
        views.UpdateBorrowedBookGenericView.as_view(),
        name="borrowed-book",
    ),
    path("hold-list/", views.UserHoldListBooksGenericView.as_view(), name="hold-list"),
]
