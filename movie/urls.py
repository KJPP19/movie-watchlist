from django.urls import path
from .views import GenreListCreateAPI, GenreDetail, MovieCreateAPI, MovieDetail, \
                   WatchListCreateAPI, WatchListDetail, ReviewsAPI, \
                   ReviewMovieAPI, ReviewDetail, ReviewDetailPutDelete, MovieListAPI, WatchListAPI, StreamPlatformAPI, \
                   StreamPlatformDetail


urlpatterns = [
    path('stream-platform/', StreamPlatformAPI.as_view()),
    path('stream-platform/<int:pk>/', StreamPlatformDetail.as_view()),
    path('genre/', GenreListCreateAPI.as_view()),
    path('genre-detail/<int:pk>/', GenreDetail.as_view()),
    path('movie/', MovieCreateAPI.as_view()),
    path('movie-list/', MovieListAPI.as_view()),
    path('moviedetail/<int:pk>/', MovieDetail.as_view()),
    path('watch-list/', WatchListAPI.as_view()),
    path('watch-list/create/', WatchListCreateAPI.as_view()),
    path('watch-list-detail/<int:pk>', WatchListDetail.as_view()),
    path('movie-review-list/', ReviewsAPI.as_view()),
    path('review-movie/', ReviewMovieAPI.as_view()),
    path('review-detail/<int:pk>', ReviewDetail.as_view()),
    path('review-put-delete/<int:pk>', ReviewDetailPutDelete.as_view())
]