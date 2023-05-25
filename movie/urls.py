from django.urls import path
from .views import GenreListCreateAPI, GenreDetail, MovieCreateAPI, MovieDetail, \
                   WatchListCreateAPI, WatchListDetail, ReviewsAPI, \
                   ReviewMovieAPI, ReviewDetail, ReviewDetailPutDelete, DetailedMovieListAPI, WatchListAPI, StreamPlatformAPI, \
                   StreamPlatformDetail, MovieListByGenre

"""All endpoints that have user/ can be accessed ONLY by the user's TOKEN credentials."""
urlpatterns = [
    path('stream-platforms/', StreamPlatformAPI.as_view(), name='stream-platforms'),
    path('stream-platforms/<int:pk>/', StreamPlatformDetail.as_view(), name='stream-platforms-detail'),
    path('genres/', GenreListCreateAPI.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetail.as_view(), name='genre-detail'),
    path('genres/<int:pk>/movies/', MovieListByGenre.as_view()),
    path('movies/new/', MovieCreateAPI.as_view(), name='movie-create'),
    path('movies/', DetailedMovieListAPI.as_view(), name='detailed-movie-list'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('user/<int:user_id>/watch-list/', WatchListAPI.as_view(), name='watchlist'),
    path('user/<int:user_id>/watch-list/add/', WatchListCreateAPI.as_view(), name='watchlist-add'),
    path('user/<int:user_id>/watch-list/<int:pk>/', WatchListDetail.as_view()),
    path('movie-reviews/', ReviewsAPI.as_view(), name='movie-reviews-list'),
    path('user/<int:user_id>/movie-reviews/add/', ReviewMovieAPI.as_view(), name='add-movie-review'),
    path('movie-reviews/<int:pk>/', ReviewDetail.as_view()),
    path('user/<int:user_id>/movie-reviews/<int:pk>/', ReviewDetailPutDelete.as_view())
]