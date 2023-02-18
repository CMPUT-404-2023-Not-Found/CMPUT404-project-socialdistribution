# 2023-02-18
# inbox/models.py
# For ERD refer here: https://github.com/CMPUT-404-2023-Not-Found/CMPUT404-project-socialdistribution/wiki/ERD

from django.db import models

from author.models import Author
from utils.model_abstracts import Model

class Inbox(Model):
    class TypeChoices(models.TextChoices):
        POST    = ('post', 'Post')
        LIKE    = ('like', 'Like')
        FR      = ('follow_request', 'Follow Request')
        COMMENT = ('comment', 'Comment')
    
    class W3ContextChoices(models.TextChoices):
        W3_AS=('https://www.w3.org/ns/activitystreams', 'W3 Activity Streams')

    # Identification fields
    author_id           = models.ForeignKey(to=Author, on_delete=models.CASCADE, verbose_name="Inbox Author's UUID")

    # Modification fields
    has_seen            = models.BooleanField(default=False, verbose_name='Has Seen')
    received_at         = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Received At')

    # Origin fields
    item_id             = models.URLField(blank=False, null=False, max_length=128, verbose_name='Item Node ID')
    item_author_id      = models.URLField(blank=False, null=False, max_length=128, verbose_name='Item Owner Node ID')

    # Content fields
    context             = models.URLField(choices=W3ContextChoices.choices, default=W3ContextChoices.W3_AS, max_length=128)
    summary             = models.CharField(max_length=32)
    type                = models.CharField(choices=TypeChoices.choices, default=TypeChoices.POST, max_length=32)
