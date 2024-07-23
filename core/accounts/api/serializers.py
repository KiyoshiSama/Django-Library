from rest_framework import serializers
from django.core import exceptions
from django.core.cache import cache
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "passwords don't match"})

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
        read_only_fields = ["id", "email"]


class VerificationCodeSerialzier(serializers.Serializer):

    verification_code = serializers.CharField(
        label=_("verification_code;"), write_only=True
    )

    def validate(self, attrs):
        verification_code = attrs.get("verification_code")
        request = self.context.get("request")
        user = request.user
        defined_verification_code = cache.get(str(user.id))

        if not defined_verification_code:
            raise serializers.ValidationError({"details": "you took so long!the code has expired."})
        if not user.is_first_login:
            raise serializers.ValidationError({"details": "account already confirmed"})
        if defined_verification_code != verification_code:
            raise serializers.ValidationError({"details": "Invalid activation code"})


        return attrs

    def save(self):
        request = self.context.get("request")
        user = request.user

        user.is_verified = True
        user.is_first_login = False
        user.save()
