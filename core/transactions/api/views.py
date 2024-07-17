from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from books.models import Book
from transactions.api.serializers import (
    BorrowBookSerializer,
    PutOnHoldSerializer,
    UserBorrowedBooksSerializer,
    UserHoldListBooksSerializer,
)
from transactions.models import Checkout, Hold
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BorrowBookGenericView(APIView):
    serializer_class = BorrowBookSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BorrowBookSerializer(data=request.data)
        if serializer.is_valid():
            current_book_id = serializer.validated_data.get("book").id
            book = get_object_or_404(Book, id=current_book_id)
            if book.is_available:
                checkout_data = serializer.validated_data
                checkout_data["is_returned"] = False
                checkout_data["customer"] = request.user
                book.is_available = False
                book.save()
                serializer.save()
                return Response(
                    {"details": "book successfully borrowed"},
                    status=status.HTTP_201_CREATED,
                )
            elif Checkout.objects.filter(
                customer=request.user, book=book, is_returned=False
            ).exists():
                return Response(
                    {"details": "you've already reserved this book"},
                    status=status.HTTP_200_OK,
                )

            elif Hold.objects.filter(customer=request.user, book=book).exists():
                return Response(
                    {"details": "you are already on hold list!"},
                    status=status.HTTP_200_OK,
                )
            else:
                serializer = PutOnHoldSerializer(data=request.data)
                if serializer.is_valid():
                    hold_data = serializer.validated_data
                    hold_data["customer"] = request.user
                    serializer.save()
                return Response(
                    {"details": "book is not avaiable, we'll put you on hold instead"},
                    status=status.HTTP_201_CREATED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBorrowedBooksGenericView(generics.ListAPIView):
    serializer_class = UserBorrowedBooksSerializer
    permission_classes = [IsAuthenticated]
    queryset = Checkout.objects.all()

    def get_queryset(self):
        return Checkout.objects.filter(customer=self.request.user)


class UpdateBorrowedBookGenericView(generics.RetrieveUpdateAPIView):
    serializer_class = UserBorrowedBooksSerializer
    queryset = Checkout.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, customer=self.request.user, pk=self.kwargs["pk"]
        )
        return obj


class UserHoldListBooksGenericView(generics.ListAPIView):
    serializer_class = UserHoldListBooksSerializer
    permission_classes = [IsAuthenticated]
    queryset = Checkout.objects.all()

    def get_queryset(self):
        return Checkout.objects.filter(customer=self.request.user)
