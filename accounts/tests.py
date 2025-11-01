"""
Unit tests for accounts app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test cases for User model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """Test user is created correctly."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_handle_generation(self):
        """Test handle is auto-generated."""
        self.assertIsNotNone(self.user.handle)
        self.assertTrue(self.user.handle.startswith('@'))
    
    def test_profile_creation(self):
        """Test profile is created automatically."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsNotNone(self.user.profile)


class AuthAPITestCase(TestCase):
    """Test cases for authentication API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_user(self):
        """Test user registration endpoint."""
        url = reverse('auth_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
    
    def test_register_with_mismatched_passwords(self):
        """Test registration fails with mismatched passwords."""
        url = reverse('auth_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'differentpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_token(self):
        """Test JWT token generation."""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_get_token_with_invalid_credentials(self):
        """Test token generation fails with invalid credentials."""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_profile_endpoint_requires_authentication(self):
        """Test profile endpoint requires authentication."""
        url = reverse('user_profile', kwargs={'username': 'testuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_profile_endpoint_authenticated(self):
        """Test profile endpoint with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('user_profile', kwargs={'username': 'testuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
