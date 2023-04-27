from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        # email will be the login credential, initially it was username.
        if not email:
            raise ValueError('Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        # create and saves superuser with the given credentials
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=120)
    # user role must be specified to be use for user permissions
    # purpose of the ROLE_CHOICES is users can only pick a valid role
    ROLE_CHOICES = (
        ('watcher', 'Watcher'),
        ('reviewer', 'Reviewer'),
        ('visitor', 'Visitor'),
        ('admin', 'Admin'))
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'role']

    def __str__(self):
        return self.email


class LogInUser(models.Model):
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=50)
