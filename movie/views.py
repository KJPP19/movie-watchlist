from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Genre, Movie, WatchList, MovieReview, StreamPlatform
from .serializers import GenreSerializer, MovieSerializer, WatchListSerializer, MovieReviewSerializer, \
    StreamPlatformSerializer, IsWatcher, IsReviewer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter


class GenreListCreateAPI(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        genre_name = request.data.get('name')
        if Genre.objects.filter(name=genre_name).exists():
            return Response({'message': 'genre already exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GenreSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'genre created'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformAPI(APIView):
    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream_platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        stream_platform_name = request.data.get('name')
        if StreamPlatform.objects.filter(name=stream_platform_name).exists():
            return Response({'message': 'stream platform already exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StreamPlatformSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'stream platform created'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetail(APIView):
    def get(self, request, pk):
        stream_platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = StreamPlatformSerializer(stream_platform)
        return Response(serializer.data)

    def put(self, request, pk):
        stream_platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = StreamPlatformSerializer(stream_platform, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'stream platform updated'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        stream_platform = get_object_or_404(StreamPlatform, pk=pk)

        try:
            stream_platform.delete()
            return Response({'message': 'stream platform deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieListAPI(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'genre__name', 'stream_platform__name')


class MovieCreateAPI(APIView):

    def post(self, request):
        movie_title = request.data.get('title')
        if Movie.objects.filter(title=movie_title).exists():
            return Response({'message': 'movie already exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MovieSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'movie created'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieDetail(APIView):

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'movie updated'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        try:
            movie.delete()
            return Response({'message': 'movie deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WatchListAPI(ListAPIView):
    serializer_class = WatchListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWatcher]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['movie__title']

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


class WatchListCreateAPI(APIView):

    """to access the watchlist user must be token authenticated AND has a role of 'watcher'
    if user has different roles, it will return a message based on the custom permission created
    it should satisfy both permission classes"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWatcher]

    def post(self, request):
        movie_title = request.data.get('movie_title')
        # print(movie_title) verify the input data
        if WatchList.objects.filter(movie__title=movie_title, user=request.user).exists():
            return Response({'message': 'movie already exist in your watchlist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(title=movie_title)
        except Movie.DoesNotExist:
            return Response({'message': 'movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, movie=movie)
            return Response({'message': 'movie was added to your watchlist'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WatchListDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWatcher]

    def get(self, request, pk):
        watchlist_item = get_object_or_404(WatchList, user=request.user, pk=pk)
        serializer = WatchListSerializer(watchlist_item)
        return Response(serializer.data)

    def put(self, request, pk):
        watchlist_item = get_object_or_404(WatchList, user=request.user, pk=pk)
        movie_title = request.data.get('movie_title', watchlist_item.movie.title)
        if WatchList.objects.filter(movie__title=movie_title, user=request.user).exclude(pk=pk).exists():
            return Response({'message': 'this movie already exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(title=movie_title)
        except Movie.DoesNotExist:
            return Response({'message': 'movie does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = WatchListSerializer(watchlist_item, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, movie=movie)
            return Response({'message': 'watchlist updated'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        watchlist_item = get_object_or_404(WatchList, user=request.user, pk=pk)

        try:
            watchlist_item.delete()
            return Response({'message': 'movie deleted from watchlist'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewsAPI(ListAPIView):

    queryset = MovieReview.objects.all()
    serializer_class = MovieReviewSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['movie__title', 'review', 'reviewed_by__email']


class ReviewMovieAPI(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsReviewer | IsWatcher]

    def post(self, request):
        movie_title = request.data.get('movie_title')
        if MovieReview.objects.filter(movie__title=movie_title, reviewed_by=request.user).exists():
            return Response({'message': 'movie already exist in your review'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(title=movie_title)
        except Movie.DoesNotExist:
            return Response({'message': 'movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieReviewSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(reviewed_by=request.user, movie=movie)
            return Response({'message': 'review for the movie has been added'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewDetail(APIView):

    def get(self, request, pk):
        review = get_object_or_404(MovieReview, pk=pk)
        serializer = MovieReviewSerializer(review)
        return Response(serializer.data)


class ReviewDetailPutDelete(APIView):

    """reviewer only have the permission to PUT and DELETE review"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsReviewer | IsWatcher]

    def put(self, request, pk):
        review = get_object_or_404(MovieReview, reviewed_by=request.user, pk=pk)
        serializer = MovieReviewSerializer(review, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(reviewed_by=request.user)
            return Response({'message': 'review updated'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        review = get_object_or_404(MovieReview, reviewed_by=request.user, pk=pk)

        try:
            review.delete()
            return Response({'message': 'review for the movie has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
