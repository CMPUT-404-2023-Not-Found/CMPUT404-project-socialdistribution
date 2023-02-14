# 2023-02-13
# author/models.py

from django.db import models

from utils.model_abstracts import Model

class Author(Model):
    # Required fields
    username        = models.CharField(max_length=32, unique=True)
    password        = models.CharField(max_length=64)

    # Modification fields
    createdOn       = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Creation On")
    lastModified    = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last Modified On")
    rev             = models.IntegerField(default=0)
    
    # Personalization fields
    displayName     = models.CharField(default="", max_length=128, verbose_name="Display Name")
    github          = models.URLField(default="", max_length=128, verbose_name="GitHub")
    host            = models.URLField(max_length=128)
    profileImage    = models.URLField(default="", max_length=128, verbose_name="Profile Image")

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f'{self.username}'

