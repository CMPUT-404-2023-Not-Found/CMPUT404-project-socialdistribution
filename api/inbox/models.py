# 2023-02-18
# inbox/models.py
# For ERD refer here: https://github.com/CMPUT-404-2023-Not-Found/CMPUT404-project-socialdistribution/wiki/ERD

from django.apps import apps
from django.db import models

from author.models import Author
from utils.model_abstracts import Model

def create_summary():
    pass

class Inbox(Model):
    class TypeChoices(models.TextChoices):
        POST    = ('post', 'Post')
        LIKE    = ('like', 'Like')
        FR      = ('follow', 'Follow Request')
        COMMENT = ('comment', 'Comment')
    
    class W3ContextChoices(models.TextChoices):
        W3_AS=('https://www.w3.org/ns/activitystreams', 'W3 Activity Streams')

    # Identification fields
    author              = models.ForeignKey(to=Author, on_delete=models.CASCADE, verbose_name="Inbox Owner")

    # Modification fields
    received_at         = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Received At')

    # Origin fields
    object_id             = models.URLField(blank=False, null=False, max_length=512, verbose_name='Object Node ID')
    sender_author_id      = models.URLField(blank=False, null=False, max_length=512, verbose_name='Object From')

    # Content fields
    context             = models.URLField(choices=W3ContextChoices.choices, default=W3ContextChoices.W3_AS, max_length=128)
    summary             = models.CharField(max_length=512)
    type                = models.CharField(choices=TypeChoices.choices, default=TypeChoices.POST, max_length=32)

    def __str__(self):
        if self.author.display_name:
            return f'{self.author.display_name} - {self.summary}'
        else:
            return f'{self.author.username} - {self.summary}'
