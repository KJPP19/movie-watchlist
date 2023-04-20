from django.urls import path
from .views import RegisterAPI, LogInAPI


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LogInAPI.as_view(), name='login')
]