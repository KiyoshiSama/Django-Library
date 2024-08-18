from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.api import views

app_name = "accounts-api"

urlpatterns = [
    path("all-accounts", views.ViewAllUsersGenericView.as_view(), name="accounts-view"),
    path("all-accounts/<int:pk>", views.UserProfileGenericView.as_view(), name="all-accounts"),
    path(
        "token-create/",
        views.CustomTokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path("token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("create-account/", views.RegisterUserAPIView.as_view(), name="create-account"),
    path(
        "active-account/",
        views.ActiveAccountGenericApiView.as_view(),
        name="active-account",
    ),
]
