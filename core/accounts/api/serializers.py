from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import exceptions
from django.core.cache import cache
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from accounts.api.utils import validate_verification_code


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": _("passwords don't match")})

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
        validate_verification_code(user, verification_code)
        return attrs

    def save(self):
        request = self.context.get("request")
        user = request.user

        user.is_verified = True
        user.is_first_login = False
        user.save()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        # if not self.user.is_verified:
        #     raise serializers.ValidationError({"details": _("user is not verified")})

        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data
