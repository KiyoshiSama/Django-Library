from django.core.cache import cache
from rest_framework import serializers


def validate_verification_code(user, verification_code):
    defined_verification_code = cache.get(str(user.id))

    if not defined_verification_code:
        raise serializers.ValidationError(
            {"details": "you took so long! the code has expired."}
        )
    if not user.is_first_login:
        raise serializers.ValidationError({"details": "account already confirmed"})
    if defined_verification_code != verification_code:
        raise serializers.ValidationError({"details": "Invalid activation code"})
