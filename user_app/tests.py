from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your tests here.
class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "NewPassword01@",
            "password2": "NewPassword01@",
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):        #creating a new user
        self.user = User.objects.create_user(
            username = "example",
            password = "NewPassword123"
        )
        
    def test_login(self):
        data = {                    #login in a user
            "username": "example",
            "password": "NewPassword123"
        }
        
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_logout(self):
        self.token = Token.objects.get(user__username = "example")      #obtaining the token. 
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)