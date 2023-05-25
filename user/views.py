from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomUserSerializer, LogInUserSerializer
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterAPI(APIView):

    @swagger_auto_schema(operation_summary="fetch registered user")
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CustomUserSerializer,
                         operation_summary="This endpoint creates a new user",
                         operation_description="user role choices are watcher, reviewer, visitor",
                         responses={
                             status.HTTP_201_CREATED: openapi.Response(description="account created successfully"),
                             status.HTTP_400_BAD_REQUEST: openapi.Response(description="bad request")})
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogInAPI(APIView):

    @swagger_auto_schema(request_body=LogInUserSerializer,
                         operation_summary="This endpoint generates token to a specific registered user",
                         operation_description="registered email and password is the required credentials",
                         responses={
                             status.HTTP_200_OK: openapi.Response(description="Token generated successfully"),
                             status.HTTP_404_NOT_FOUND: openapi.Response(description="credentials is incorrect")})
    def post(self, request):
        serializer = LogInUserSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if not user:
                return Response({'message': 'invalid email and password'}, status=status.HTTP_404_NOT_FOUND)
            token = Token.objects.get_or_create(user=user)
            return Response({'message': 'successfully logged in', 'token': user.auth_token.key},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

