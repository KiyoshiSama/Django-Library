from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from accounts.api.serializers import (
    UserProfileSerializer,
    UserRegisterSerializer,
    VerificationCodeSerialzier,
    CustomTokenObtainPairSerializer,
)
from accounts.models.users import User
from accounts.tasks import send_verification_code_task


class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_code_task.delay(user.id)
        return Response(
            {
                "detail": _(
                    "Account created and Activation code has successfully been sent"
                ),
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class ActiveAccountGenericApiView(generics.GenericAPIView):
    serializer_class = VerificationCodeSerialzier
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": _("Account confirmed successfully")},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ViewAllUsersGenericView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, customer=self.request.user, pk=self.kwargs["pk"]
        )
        return obj

class UserProfileGenericView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, email=self.request.user.email)
        return obj
