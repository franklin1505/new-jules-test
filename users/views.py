from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

# LoginView will use TokenObtainPairView, so no explicit class needed here unless customization is required.
# We will directly use TokenObtainPairView in urls.py
