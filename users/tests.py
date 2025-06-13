from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('token_obtain_pair')
        # Username and password are now auto-generated, so remove them from fixed user_data
        self.user_register_data = {
            'email': 'test@example.com',
            'user_type': 'client'
        }
        self.admin_register_data = {
            'email': 'admin@example.com',
            'user_type': 'administrator'
        }

    def test_user_registration(self):
        """
        Ensure we can register a new user and get auto-generated credentials.
        """
        response = self.client.post(self.register_url, self.user_register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        # Check response content
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.user_register_data['email'])
        self.assertIn('username', response.data)
        self.assertIsInstance(response.data['username'], str)
        self.assertTrue(len(response.data['username']) > 0)
        self.assertIn('generated_password', response.data)
        self.assertIsInstance(response.data['generated_password'], str)
        self.assertTrue(len(response.data['generated_password']) > 0)

        # Check database entry
        db_user = User.objects.get(email=self.user_register_data['email'])
        self.assertEqual(db_user.username, response.data['username'])
        self.assertEqual(db_user.user_type, self.user_register_data['user_type'])


    def test_admin_registration(self):
        """
        Ensure we can register a new admin user and get auto-generated credentials.
        """
        response = self.client.post(self.register_url, self.admin_register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        # Check response content
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.admin_register_data['email'])
        self.assertIn('username', response.data)
        self.assertIsInstance(response.data['username'], str)
        self.assertTrue(len(response.data['username']) > 0)
        self.assertIn('generated_password', response.data)
        self.assertIsInstance(response.data['generated_password'], str)
        self.assertTrue(len(response.data['generated_password']) > 0)

        # Check database entry
        db_user = User.objects.get(email=self.admin_register_data['email'])
        self.assertEqual(db_user.username, response.data['username'])
        self.assertEqual(db_user.user_type, self.admin_register_data['user_type'])


    def test_user_login(self):
        """
        Ensure a registered user can log in using auto-generated credentials.
        """
        # First, register the user
        register_response = self.client.post(self.register_url, self.user_register_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # Get generated credentials from registration response
        generated_username = register_response.data['username']
        generated_password = register_response.data['generated_password']

        # Then, attempt to log in
        login_data = {'username': generated_username, 'password': generated_password}
        login_response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(login_response.status_code, status.HTTP_200_OK, login_response.data)
        self.assertTrue('access' in login_response.data)
        self.assertTrue('refresh' in login_response.data)

    def test_login_invalid_credentials(self):
        """
        Ensure login fails with invalid credentials.
        """
        login_data = {'username': 'nonexistentuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

from django.test import TestCase
from .utils import generate_random_password, generate_random_username
# User model is already imported above for APITestCase
import re
import string # For string.punctuation
from unittest.mock import patch

class TestPasswordGeneration(TestCase):
    def test_password_length(self):
        """Test that generated passwords have the specified length."""
        self.assertEqual(len(generate_random_password()), 12) # Default length
        self.assertEqual(len(generate_random_password(length=16)), 16)
        self.assertEqual(len(generate_random_password(length=8)), 8)

    def test_password_complexity(self):
        """Test that generated passwords meet complexity requirements."""
        for _ in range(20): # Test a few generated passwords
            password = generate_random_password(length=12)
            self.assertTrue(re.search(r'[a-z]', password), "Password should contain a lowercase letter.")
            self.assertTrue(re.search(r'[A-Z]', password), "Password should contain an uppercase letter.")
            self.assertTrue(re.search(r'[0-9]', password), "Password should contain a digit.")
            # Check for punctuation. string.punctuation is "!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
            # We need to escape special characters if using them directly in re.search, or check char by char.
            # An easier way is to check if any character from string.punctuation is in the password.
            self.assertTrue(any(char in string.punctuation for char in password), "Password should contain a punctuation character.")

class TestUsernameGeneration(TestCase):
    def test_username_generation_success(self):
        """Test successful username generation."""
        email_prefix = "testuser"
        username = generate_random_username(email_prefix)
        self.assertIsNotNone(username)
        # Username generation logic takes min(len(email_prefix), 150 - length -1) for the prefix part.
        # Default length for random part is 8. So prefix_len_to_use = min(8, 150 - 8 - 1) = min(8, 141) = 8
        # So it should start with "testuser" if "testuser" is short enough, or a part of it.
        self.assertTrue(username.startswith(email_prefix[:min(len(email_prefix), 150-8-1)]))
        # Ensure it's unique enough for creation (actual creation test is separate)
        self.assertFalse(User.objects.filter(username=username).exists())

    def test_username_generation_prefix_handling(self):
        """Test username generation with a specific prefix and length."""
        email_prefix = "longprefixbyemail"
        random_part_length = 4
        # prefix_len_to_use = min(len(longprefixbyemail), 150 - 4 - 1) = min(17, 145) = 17
        # So, the username should start with "longprefixbyemail"
        username = generate_random_username(email_prefix, length=random_part_length)
        self.assertIsNotNone(username)
        expected_prefix_part = email_prefix[:min(len(email_prefix), 150 - random_part_length -1)]
        self.assertTrue(username.startswith(expected_prefix_part))
        self.assertEqual(len(username), len(expected_prefix_part) + random_part_length)


    @patch('users.utils.User.objects.filter')
    def test_username_uniqueness_retry(self, mock_filter):
        """Test that username generation retries if a username exists."""
        # Simulate username 'testa' and 'testb' exist, 'testc' is free.
        # The generated username is prefix + random suffix.
        # We need to control the random suffix to make this test predictable,
        # or mock the whole generate_random_username internal random part.
        # For simplicity, let's assume the first part of the prefix is 'test'
        # and the random part generates 'a', then 'b', then 'c'.
        # The mock needs to return an object with an `exists()` method.

        # Side effect for mock_filter.exists()
        # 1st call (e.g. for 'test_rand1'): True (exists)
        # 2nd call (e.g. for 'test_rand2'): True (exists)
        # 3rd call (e.g. for 'test_rand3'): False (does not exist)
        mock_filter_instance = mock_filter.return_value
        mock_filter_instance.exists.side_effect = [True, True, False]

        email_prefix = "test"
        username = generate_random_username(email_prefix, length=5, max_attempts=3) # length of random part

        self.assertIsNotNone(username)
        # It should have tried 3 times for exists()
        self.assertEqual(mock_filter_instance.exists.call_count, 3)
        # The filter itself is called once per attempt in generate_random_username
        self.assertEqual(mock_filter.call_count, 3)


    @patch('users.utils.User.objects.filter')
    def test_username_generation_failure_after_max_attempts(self, mock_filter):
        """Test that username generation returns None after max attempts if all are taken."""
        mock_filter_instance = mock_filter.return_value
        mock_filter_instance.exists.return_value = True # Always simulate username exists

        email_prefix = "test"
        max_attempts = 3
        username = generate_random_username(email_prefix, max_attempts=max_attempts)

        self.assertIsNone(username)
        self.assertEqual(mock_filter.call_count, max_attempts)
        self.assertEqual(mock_filter_instance.exists.call_count, max_attempts)

    def test_username_creation_with_generated_name(self):
        """Test creating a user with a successfully generated username."""
        email_prefix = "newuser"
        # Ensure we are testing with an email that doesn't already exist from other tests
        email = f"{email_prefix}@example.com"

        # Clean up any user that might interfere from other tests if email is reused
        User.objects.filter(email=email).delete()

        username = generate_random_username(email_prefix)
        self.assertIsNotNone(username)

        # Try to create a user with this username
        try:
            user = User.objects.create_user(username=username, password="testpassword", email=email)
            self.assertIsNotNone(user)
            self.assertEqual(user.username, username)
            self.assertEqual(user.email, email)
        except Exception as e:
            self.fail(f"User creation failed with generated username '{username}': {e}")
        finally:
            # Clean up the created user
            User.objects.filter(username=username).delete()
