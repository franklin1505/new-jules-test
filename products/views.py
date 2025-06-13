from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can access

    # Optional: Customize permissions further if needed, e.g.,
    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         return [permissions.AllowAny()] # Allow anyone to view
    #     return [permissions.IsAdminUser()] # Only admins can create, update, delete
