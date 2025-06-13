from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('token_obtain_pair')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'user_type': 'client'
        }
        self.admin_data = {
            'username': 'testadmin',
            'email': 'admin@example.com',
            'password': 'testpassword123',
            'user_type': 'administrator'
        }

    def test_user_registration(self):
        """
        Ensure we can register a new user.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().user_type, 'client')

    def test_admin_registration(self):
        """
        Ensure we can register a new admin user.
        """
        response = self.client.post(self.register_url, self.admin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testadmin')
        self.assertEqual(User.objects.get().user_type, 'administrator')

    def test_user_login(self):
        """
        Ensure a registered user can log in and get tokens.
        """
        # First, register the user
        self.client.post(self.register_url, self.user_data, format='json')

        # Then, attempt to log in
        login_data = {'username': self.user_data['username'], 'password': self.user_data['password']}
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_login_invalid_credentials(self):
        """
        Ensure login fails with invalid credentials.
        """
        login_data = {'username': 'nonexistentuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
