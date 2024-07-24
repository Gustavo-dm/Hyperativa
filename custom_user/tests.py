from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser

class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')  # Atualizado para o nome correto

    def test_register_user_success(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'securepassword',
            'username': 'newuser'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'newuser@example.com')

    def test_register_user_invalid_data(self):
        # Missing password
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_register_user_existing_email(self):
        # Register first user
        data = {
            'email': 'existinguser@example.com',
            'password': 'securepassword',
            'username': 'existinguser'
        }
        self.client.post(self.url, data, format='json')
        
        # Try to register another user with the same email
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_register_user_missing_fields(self):
        # Missing email
        data = {
            'password': 'securepassword',
            'username': 'newuser'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

        # Missing username
        data = {
            'email': 'newuser@example.com',
            'password': 'securepassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
