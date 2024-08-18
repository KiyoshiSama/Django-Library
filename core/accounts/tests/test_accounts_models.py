import pytest
from django.core.exceptions import ValidationError
from accounts.models.users import User


@pytest.mark.django_db
class TestUserModel:

    @pytest.mark.django_db
    def test_create_user(self, create_user, user_data):
        user = create_user
        assert user.email == user_data["email"]
        assert user.check_password(user_data["password"])
        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_verified

    @pytest.mark.django_db
    def test_create_superuser(self, create_superuser, user_data):
        superuser = create_superuser
        assert superuser.email == user_data["email"]
        assert superuser.check_password(user_data["password"])
        assert superuser.first_name == user_data["first_name"]
        assert superuser.last_name == user_data["last_name"]
        assert superuser.is_staff
        assert superuser.is_superuser
        assert superuser.is_verified

    @pytest.mark.django_db
    def test_create_user_without_email(self, user_data):
        user_data.pop("email")
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_user(**user_data, email="")
        assert str(excinfo.value) == "Wrong email!"

    @pytest.mark.django_db
    def test_create_superuser_without_is_staff(self, user_data):
        user_data.update({"is_staff": False})
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_superuser(**user_data)
        assert str(excinfo.value) == "Superuser must have is_staff=True."

    @pytest.mark.django_db
    def test_create_superuser_without_is_superuser(self, user_data):
        user_data.update({"is_superuser": False})
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_superuser(**user_data)
        assert str(excinfo.value) == "Superuser must have is_superuser=True."

    @pytest.mark.django_db
    def test_create_superuser_without_is_verified(self, user_data):
        user_data.update({"is_verified": False})
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_superuser(**user_data)
        assert str(excinfo.value) == "Superuser must have is_verified=True."
