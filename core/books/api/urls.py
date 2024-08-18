from django.urls import path, include
from books.api.routers import router

app_name = "books-api"

urlpatterns = [
    path("", include(router.urls)),
]
