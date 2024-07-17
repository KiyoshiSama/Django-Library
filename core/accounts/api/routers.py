from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet
from django.urls import path,include

router = DefaultRouter()
router.register(r'accounts', UserProfileViewSet, basename='accounts')

