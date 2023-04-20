from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomUserSerializer, LogInUserSerializer
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers


class RegisterAPI(APIView):

    # get method is used to verify and check registered account, this can be removed.
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'account created'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogInAPI(APIView):

    def post(self, request):
        serializer = LogInUserSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if not user:
                return Response({'message': 'invalid email and password'}, status=status.HTTP_404_NOT_FOUND)
            token = Token.objects.get_or_create(user=user)
            return Response({'message': 'successfully logged in', 'token': user.auth_token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

