from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import CustomUser, LogInUser
from django.contrib.auth.hashers import make_password


class RegisterAndLogInApiTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "johndoe@sample.com",
             "password": make_password("123456789"),
            "first_name": "john",
            "last_name": "doe",
            "username": "jd",
            "role": "watcher"
        }
        self.user = CustomUser.objects.create(**self.user_data)
        self.register_url = reverse('register')
        self.login_url = reverse('login')
    
    def test_register_user(self):
        new_user_data = {
            "email": "testuser@sample.com",
             "password": "123456789",
            "first_name": "john",
            "last_name": "doe",
            "username": "TU",
            "role": "reviewer"
        }
        response = self.client.post(self.register_url, data=new_user_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(response.data['email'], 'testuser@sample.com')

    def test_register_existing_user(self):
        response = self.client.post(self.register_url, data=self.user_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['error']['email'][0]), 'user with this email already exists.')

    def test_login_valid_credentials(self):
        login_data = {
            "email": "johndoe@sample.com",
            "password": "123456789"
        }
        response = self.client.post(self.login_url, data=login_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'successfully logged in')
        self.assertIn('token', response.data)
    
    def test_login_invalid_credentials(self):
        login_data = {
            "email": "sampleuser@sample.com",
            "password": "123456789"
        }
        response = self.client.post(self.login_url, data=login_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'invalid email and password')
