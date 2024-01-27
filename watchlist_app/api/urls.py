from django.urls import path, include
from watchlist_app.api.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamPlatFormAV, basename = 'streamplatform')

urlpatterns = [
    path('', WatchListList.as_view(), name = 'movie-list'),
    path('watchlist/<int:pk>/', WatchListDetails.as_view(), name = 'movie-detail'),
    path('list2', WatchListAV.as_view(), name='movie-details'),

# ReviewsListDetails
    path('streamplatform/', StreamPlatFormList.as_view(), name = 'streamplatform'),
    # path('streamplatform/<int:pk>/reviews/', StreamPlatFormDetails.as_view(), name = 'streamplatform-detail'),          #allows me to access alll reviews for a particular movie. 
    
    path('', include(router.urls)),
    
    path('stream/<int:pk>/reviews/', ReviewsList.as_view(), name = 'review-detials'),            #accessing individual reviews. 
    path('stream/<str:pk>/reviews-create', ReviewsCreate.as_view(), name = 'review-create'),
    path('review/<int:pk>/', ReviewsListDetails.as_view(), name = "reviews"),
    
    path('reviews/', UserReviews.as_view(), name = 'user')
]

