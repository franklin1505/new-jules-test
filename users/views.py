from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.last_logout_time = timezone.now()
        user.save(update_fields=['last_logout_time'])
        # In a real application with token blacklisting, you would add the token to a blacklist here.
        # For example, if using `rest_framework_simplejwt.token_blacklist`, you might do:
        # from rest_framework_simplejwt.tokens import RefreshToken
        # try:
        #     refresh_token = request.data["refresh"]
        #     token = RefreshToken(refresh_token)
        #     token.blacklist()
        # except Exception as e:
        #     # Handle cases where refresh token is not provided or is invalid
        #     pass # Or log the error
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
