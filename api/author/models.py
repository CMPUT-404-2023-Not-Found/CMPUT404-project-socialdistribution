# 2023-02-13
# author/models.py

from django.db import models

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-16 retrieved on 2023-02-14, to Youtube crycetruly
# video here:
# https://youtu.be/SP5je7d3MFA
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
import uuid

class AuthorManager(BaseUserManager):
    def create_author(self, username, password):
        if username is None:
            raise TypeError('You must provide a username')
        if password is None:
            raise TypeError('You must provide a password')
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_author(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class Author(AbstractBaseUser, PermissionsMixin):
    # Identification fields
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host            = models.URLField(max_length=128)
    username        = models.CharField(max_length=32, unique=True, db_index=True)

    # Modification fields
    createdAt       = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Created At')
    isActive        = models.BooleanField(default=False)
    updatedAt       = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Last Updated At')
    rev             = models.IntegerField(default=0)
    
    # Personalization fields
    displayName     = models.CharField(default='', max_length=128, verbose_name='Display Name')
    github          = models.URLField(default='', max_length=128, verbose_name='GitHub')
    profileImage    = models.URLField(default='', max_length=128, verbose_name='Profile Image')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['host']

    objects = AuthorManager()

    def __str__(self):
        return f'{self.username}'

    def tokens(self):
        return ''
