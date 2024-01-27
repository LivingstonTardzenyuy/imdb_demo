from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from watchlist_app.models import *

from watchlist_app.api import serializers 
from watchlist_app import models
from rest_framework.request import Request
from rest_framework.test import force_authenticate

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(username = "example", password = "Password@123")
        #Login in a user. 
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        
        self.stream = StreamPlatForm.objects.create(
            name = "netflix",
            about = ""
        )
        
    def test_streamPlatFormCreate(self):
        data = {
            "name": "kongyuylivingston",
            "about": "best movie on earth",
            "website": "www.kongnyuy.com",
        }
        
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_streamplatform_id(self):
        response = self.client.get(reverse('streamplatform-detail', args = (self.stream.id,)))      #args allow me to access the individual elements. 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    # def test_stramplatform
class WatchlistTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kongnyuy", password="Password@123")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token' + self.token.key)
        
        self.stream = StreamPlatForm.objects.create(
            name="Netflix",
            about="The movie of the gold",
            website="www.abakwa.com"
        
        )
        
        self.watchlist = models.WatchList.objects.create(platform = self.stream, title="example movies", description="Example movie", active=True)
    
    def test_watchlist_create(self):
        data = {
            "title": "Abakwa",
            "description": "the movie that will be great for all",
            "platform": self.stream,
            "active": True 
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail', args = (self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, "example movies")
        self.assertEqual(models.WatchList.objects.count(), 1)
        
    # def test_watchlist_delete(self):
    #     response = self.client.delete(reverse('movie-detail', args=(self.watchlist.id,)))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatForm.objects.create(
            name="Netflix",
            about="#1 platform",
            website="www.abakwa.com"
        )
        
        self.watchlist = models.WatchList.objects.create(
            platform = self.stream,
            title = 'the pride of abakwa',
            description = 'best movie in the city',
            active = 'True'
        )
        
        self.watchlist2 = models.WatchList.objects.create(
            platform = self.stream,
            title = 'the pride of abakwa',
            description = 'best movie in the city',
            active = 'True'
        )
        
        self.review = models.Reviews.objects.create(
            review_user = self.user,
            rating = 2,
            description = "the best of the best",
            active = True,
            watchlist = self.watchlist2
        )
        
    def test_review_create(self):
        data = {
            'review_user': self.user.pk,
            'watchlist': self.watchlist.pk,    
            'rating': 4,
            'description': "best movie in town",
            'active': 'True'
        }
        
        response = self.client.post(reverse('review-create', args = (self.watchlist.id,)), data)   #we are passing the args bc we are created a review for a particular watchlist
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Second attempt should return HTTP 400
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_create_unauth(self):
        data = {
            'review_user': self.user.pk,
            'watchlist': self.watchlist.pk,    
            'rating': 4,
            'description': "best movie in town",
            'active': 'True'
        }        
        
        # force_authenticate(request, user=self.user)
        self.client.force_authenticate(user=None)  # Set user to None for unauthenticated request
        response = self.client.post(reverse('review-create', args = (self.watchlist.id,)), data) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   
    
    def test_review_update(self):
        data = {
            'review_user': self.user.pk,
            'watchlist': self.watchlist.pk,    
            'rating': 3,
            'description': "best movie in town",
            'active': True
        }   
        response = self.client.put(reverse('reviews', args = (self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        
    
    def test_review_list(self):
        response = self.client.get(reverse('review-detials', args = (self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_review_delete(self):
        response = self.client.delete(reverse('reviews', args = (self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    
    
    def test_review_user(self):
        response = self.client.get('/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)