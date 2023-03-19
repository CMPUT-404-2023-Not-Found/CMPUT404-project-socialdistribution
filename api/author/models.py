# 2023-02-13
# author/models.py

from django.conf import settings
from django.db import models

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-16 retrieved on 2023-02-14, to Youtube crycetruly
# video here:
# https://youtu.be/SP5je7d3MFA
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
import uuid

class AuthorManager(BaseUserManager):
    def create_author(self, username, password, **extra_fields):
        """
        Create an author entity
        """
        if username is None:
            raise TypeError('You must provide a username')
        if password is None:
            raise TypeError('You must provide a password')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    # This code is modified from an article from Michael Herman on 2023-01-22 retrieved on 2023-02-15, to testdriven.io
    # article here:
    # https://testdriven.io/blog/django-custom-user-model/
    def create_superuser(self, username, password, **extra_fields):
        """
        Inherit an author and include superuser status
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_author(username, password, **extra_fields)

class Author(AbstractBaseUser, PermissionsMixin):
    # Identification fields
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host                = models.URLField(default=settings.APP_URL, max_length=128)
    username            = models.CharField(max_length=32, unique=True, db_index=True)

    # Modification fields
    created_at          = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Created At')
    updated_at          = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Last Updated At')
    rev                 = models.IntegerField(default=0)
    
    # Personalization fields
    display_name        = models.CharField(blank=True, default='', max_length=128, verbose_name='Display Name')
    github              = models.URLField(blank=True, default='', max_length=128, verbose_name='GitHub')
    profile_image       = models.URLField(blank=True, default='', max_length=128, verbose_name='Profile Image')

    # System Fields
    is_staff            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['host']

    objects = AuthorManager()

    def __str__(self):
        return f'{self.id}'
    
    def get_node_id(self):
        return f'{self.host}/api/authors/{self.id}'
