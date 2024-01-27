from rest_framework.response import Response
from rest_framework.decorators import api_view
from watchlist_app.models import WatchList, StreamPlatForm, Reviews
from watchlist_app.api.serializers import WatchListSerializers, StreamPlatFormSerializers, ReviewsSerializers
from django.shortcuts import redirect
from rest_framework import status

from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle 
from watchlist_app.api.throttle import ReviewsCreateThrottle, ReviewListThrottle
from rest_framework import filters
import django_filters.rest_framework
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from watchlist_app.api.pagination import LimitOffSetPaganationAV, WatchListCPagination



class UserReviews(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewsSerializers
    throttle_classes = [ReviewListThrottle]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Reviews.objects.filter(review_user__username = username)
    

class ReviewsList(generics.ListAPIView):
    # queryset = Reviews.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewsSerializers 
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'rating', 'active']

    def get_queryset(self):             #overwritting since  we have a foreign key that we need to obtain. 
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist = pk)

class ReviewsCreate(generics.CreateAPIView):
    serializer_class = ReviewsSerializers 
    permission_classes = [IsAuthenticated]  
    throttle_classes = [ReviewsCreateThrottle]  
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        user = self.request.user

        existing_review = Reviews.objects.filter(review_user=user, watchlist=pk).first()

        if existing_review:
            return Response({"detail": "You have already reviewed this movie."}, status=status.HTTP_400_BAD_REQUEST)

        movie = WatchList.objects.get(pk=pk)
        serializer.save(review_user=user, watchlist=movie)

class ReviewsListDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializers
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class StreamPlatFormAV(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = StreamPlatForm.objects.all()
    serializer_class = StreamPlatFormSerializers 

class StreamPlatFormList(APIView):
    permission_classes = [ReviewUserOrReadOnly]

    def get(self, request, format = None):
        streamplatform = StreamPlatForm.objects.all()
        serializers = StreamPlatFormSerializers(streamplatform, many = True, context = {'request': request})
        return Response(serializers.data, status = status.HTTP_200_OK)


    def post(self, request):
        serializer = StreamPlatFormSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

class StreamPlatFormDetails(APIView):
    def get(self, request, pk):
        try:
            streamplatform = StreamPlatForm.objects.get(pk=pk)
        except StreamPlatForm.DoesNotExist:
            return Response({"error" : "StreamPlatform does not exists"}, status = status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatFormSerializers(streamplatform, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk):
        streamplatform = StreamPlatForm.objects.get(pk = pk)
        serializer = StreamPlatFormSerializers(streamplatform, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        streamplatform = StreamPlatForm.objects.get(pk = pk)
        streamplatform.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class WatchListAV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializers
    # filter_backends = [DjangoFilterBackend, SearchFilter, filters.OrderingFilter]
    # filter_fields = ['title', 'platform__name']
    # search_fields = ['=title', '^platform__name']   #= means exact match,   ^ means match start letter. 
    # ordering_fields = ['title']
    pagination_class = WatchListCPagination


class WatchListList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, format = None):
        watchlist = WatchList.objects.all()
        serializers = WatchListSerializers(watchlist, many = True)
        return Response(serializers.data, status = status.HTTP_200_OK)

    def post(self, request):
        serializers = WatchListSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetails(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist:
            return Response({"error": "WatchList does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializers = WatchListSerializers(watchlist)
        return Response(serializers.data, status = status.HTTP_200_OK)


    def put(self, request, pk):
        watchlist = WatchList.objects.get(pk = pk)
        serializers = WatchListSerializers(watchlist, data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        watchlist = WatchList.objects.get(pk = pk)
        watchlist.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
