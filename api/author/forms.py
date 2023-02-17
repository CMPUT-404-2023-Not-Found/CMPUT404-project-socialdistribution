# 2023-02-15
# author/forms.py

# This code is modified from an article from Michael Herman on 2023-01-22 retrieved on 2023-02-15, to testdriven.io
# article here:
# https://testdriven.io/blog/django-custom-user-model/#forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Author

class AuthorCreationForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ('username', 'host', 'display_name', 'github', 'profile_image')

class AuthorChangeForm(UserChangeForm):
    class Meta:
        model = Author
        fields = ('username', 'host', 'display_name', 'github', 'profile_image')