from rest_framework import serializers
from .models import CustomUser, LogInUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['email']:
            if CustomUser.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('this email was already taken')

        if data['username']:
            if CustomUser.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('this username was already taken')
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data['email'],
                                              first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'],
                                              username=validated_data['username'],
                                              role=validated_data['role'],
                                              password=validated_data['password'])
        return user


class LogInUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogInUser
        fields = ['id', 'email', 'password']
