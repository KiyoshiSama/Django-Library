from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from accounts.api.serializers import (
    UserProfileSerializer,
    UserRegisterSerializer,
    VerificationCodeSerialzier,
)
from accounts.models.users import User
from accounts.tasks import send_activation_email


class RegisterUserAPIView(generics.GenericAPIView):

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.save()
        email = serializer.validated_data["email"]
        
        try:
            send_activation_email.delay(user.id, email)
            data = {"User email": user.email, "details": "Activation email sent successfully"}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"details": f"Failed to send activation email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
                {"detail": "Account confirmed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileGenericView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, email=self.request.user.email)

        return obj
