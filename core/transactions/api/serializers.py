from rest_framework import serializers
from transactions.models import Checkout, Hold


class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ["start_time", "end_time", "book", "customer", "is_returned"]
        read_only_fields = ["is_returned", "customer"]


class PutOnHoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hold
        fields = ["start_time", "end_time", "book", "customer"]
        read_only_fields = ["customer"]

    def create(self, validated_data):
        validated_data.pop("is_returned", None)
        hold = Hold.objects.create(**validated_data)
        return hold


class UserBorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ["id", "start_time", "end_time", "book", "is_returned"]
        read_only_fields = ["start_time", "end_time", "book"]


class UserHoldListBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hold
        fields = ["id", "start_time", "end_time", "book"]
        read_only_fields = ["start_time", "end_time", "book"]
