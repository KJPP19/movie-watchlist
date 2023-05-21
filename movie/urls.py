from django.urls import path
from .views import GenreListCreateAPI, GenreDetail, MovieCreateAPI, MovieDetail, \
                   WatchListCreateAPI, WatchListDetail, ReviewsAPI, \
                   ReviewMovieAPI, ReviewDetail, ReviewDetailPutDelete, DetailedMovieListAPI, WatchListAPI, StreamPlatformAPI, \
                   StreamPlatformDetail, MovieListByGenre


urlpatterns = [
    path('stream-platforms/', StreamPlatformAPI.as_view(), name='stream-platforms'),
    path('stream-platforms/<int:pk>/', StreamPlatformDetail.as_view(), name='stream-platforms-detail'),
    path('genres/', GenreListCreateAPI.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetail.as_view(), name='genre-detail'),
    path('genres/<int:pk>/movies/', MovieListByGenre.as_view()),
    path('movies/new/', MovieCreateAPI.as_view(), name='movie-create'),
    path('movies/', DetailedMovieListAPI.as_view(), name='detailed-movie-list'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('watch-list/', WatchListAPI.as_view()),
    path('watch-list/create/', WatchListCreateAPI.as_view()),
    path('watch-list-detail/<int:pk>', WatchListDetail.as_view()),
    path('movie-review-list/', ReviewsAPI.as_view()),
    path('review-movie/', ReviewMovieAPI.as_view()),
    path('review-detail/<int:pk>', ReviewDetail.as_view()),
    path('review-put-delete/<int:pk>', ReviewDetailPutDelete.as_view())
]