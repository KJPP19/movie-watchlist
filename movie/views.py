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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GenreListCreateAPI(APIView):
    @swagger_auto_schema(operation_summary="fetch the list of genre in the database",
                         responses={status.HTTP_200_OK: openapi.Response(description="successfully fetched")})
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=GenreSerializer,
                         responses={status.HTTP_201_CREATED: openapi.Response(description="genre created successfully"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")},
                         operation_summary="This endpoint creates a new genre in the database")
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
    @swagger_auto_schema(operation_summary="fetch the list of streaming platforms in database",
                         responses={status.HTTP_200_OK: openapi.Response(description="fetched successfully")})
    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream_platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=StreamPlatformSerializer,
                         operation_summary="This endpoint creates a new streaming platform(e.g.,Netflix,AppleTV,etc.",
                         operation_description="each streaming platforms have their own available movies.",
                         responses={status.HTTP_201_CREATED: openapi.Response(description="stream platform created"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
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
    @swagger_auto_schema(operation_summary="fetch specific streaming platform")
    def get(self, request, pk):
        stream_platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = StreamPlatformSerializer(stream_platform)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=StreamPlatformSerializer,
                         operation_summary="update existing streaming platforms",
                         operation_description="update all the existing fields"
                                               "(platform name, description, available movies)",
                         responses={status.HTTP_201_CREATED: openapi.Response(description="stream platform updated"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
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

    @swagger_auto_schema(operation_summary="delete specific streaming platform")
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

    @swagger_auto_schema(request_body=MovieSerializer,
                         operation_summary="This endpoint creates a new movie",
                         operation_description="A movie can have multiple genre and stream platforms,"
                                               "genre and stream platforms must be valid or in the database."
                                               "If a valid stream platform is specified, it checks whether the movie"
                                               "title exists in the available movies of a specific streaming platform.",
                         responses={status.HTTP_201_CREATED: openapi.Response(description="movie created"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
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

    @swagger_auto_schema(operation_summary="fetch specific movie")
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MovieSerializer,
                         operation_summary="This endpoint updates a specific movie",
                         operation_description="Update existing fields, "
                                               "adding a new stream platform and genre is allowed",
                         responses={status.HTTP_201_CREATED: openapi.Response(description="movie updated"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
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

    @swagger_auto_schema(operation_summary="delete specific movie platform")
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

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWatcher]

    @swagger_auto_schema(request_body=WatchListSerializer,
                         operation_summary="This endpoint creates a watchlist",
                         operation_description="to access the watchlist user must be token authenticated "
                                               "AND has a role of 'watcher if user has different roles, "
                                               "it will return a message based on the custom permission created. "
                                               "it should satisfy both permission classes",
                         responses={status.HTTP_201_CREATED: openapi.Response(description="watchlist created"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
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

    @swagger_auto_schema(request_body=WatchListSerializer,
                         operation_summary="This endpoint updates a specific watchlist",
                         operation_description="each watchlist contains movie, editing movie title is allowed as "
                                               "long as it is valid or in the database",
                         responses={status.HTTP_201_CREATED: openapi.Response(description="watchlist updated"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
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
            return Response({'message': 'watchlist updated'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(operation_summary="delete specific movie in watchlist")
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

    @swagger_auto_schema(request_body=MovieReviewSerializer,
                         operation_summary="This endpoint creates a review for specific movie",
                         operation_description="user must be token authenticated and a reviewer or watcher in"
                                               "order to create a review, ratings is limited only from 1-5 stars and "
                                               "movie review description must have at least 10 characters, "
                                               "this raises an error if these conditions were not met, ",
                         responses={status.HTTP_201_CREATED: openapi.Response(description="review created"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
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

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsReviewer | IsWatcher]

    @swagger_auto_schema(request_body=MovieReviewSerializer,
                         operation_summary="This endpoint updates a review for specific movie",
                         operation_description="update a movie review ",
                         responses={status.HTTP_201_CREATED: openapi.Response(description="review updated"),
                                    status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
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

    @swagger_auto_schema(operation_summary="delete specific movie review")
    def delete(self, request, pk):
        review = get_object_or_404(MovieReview, reviewed_by=request.user, pk=pk)

        try:
            review.delete()
            return Response({'message': 'review for the movie has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
