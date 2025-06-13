from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User # Important: Use the custom user model
from .models import Product
from rest_framework_simplejwt.tokens import RefreshToken

class ProductCRUDTests(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user_data = {
            'username': 'testuser_for_products',
            'email': 'productuser@example.com',
            'password': 'testpassword123',
            'user_type': 'client'
        }
        self.user = User.objects.create_user(**self.user_data)

        # Obtain JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.product_list_create_url = reverse('product-list') # DRF router default name
        self.sample_product_data = {'name': 'Test Product', 'description': 'A great product', 'price': '19.99'}
        self.sample_product_data_updated = {'name': 'Test Product Updated', 'description': 'An even greater product', 'price': '29.99'}


    def test_create_product_authenticated(self):
        """
        Ensure authenticated user can create a new product.
        """
        response = self.client.post(self.product_list_create_url, self.sample_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_create_product_unauthenticated(self):
        """
        Ensure unauthenticated user cannot create a product.
        """
        self.client.credentials() # Clear authentication
        response = self.client.post(self.product_list_create_url, self.sample_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_products_authenticated(self):
        """
        Ensure authenticated user can list products.
        """
        Product.objects.create(**self.sample_product_data)
        response = self.client.get(self.product_list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_products_unauthenticated(self):
        """
        Ensure unauthenticated user cannot list products (as per current permission: IsAuthenticated).
        """
        self.client.credentials() # Clear authentication
        Product.objects.create(**self.sample_product_data)
        response = self.client.get(self.product_list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_product_authenticated(self):
        """
        Ensure authenticated user can retrieve a product.
        """
        product = Product.objects.create(**self.sample_product_data)
        detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.get(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], product.name)

    def test_update_product_authenticated(self):
        """
        Ensure authenticated user can update a product.
        """
        product = Product.objects.create(**self.sample_product_data)
        detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.put(detail_url, self.sample_product_data_updated, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, self.sample_product_data_updated['name'])

    def test_delete_product_authenticated(self):
        """
        Ensure authenticated user can delete a product.
        """
        product = Product.objects.create(**self.sample_product_data)
        detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.delete(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
