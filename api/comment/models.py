# 2023-02-25
# comment/models.py

from django.db import models
from post.models import Post
from utils.model_abstracts import Model

class Comment(Model):
    MD = 'text/markdown';       PT = 'text/plain'
    CONTENT_TYPE_OPTIONS = [
        (MD,    'Markdown'),
        (PT,    'Plain Text'),
    ]

    # Identification fields
    post            = models.ForeignKey(to=Post, on_delete=models.CASCADE, verbose_name="Post's id")
    author          = models.URLField(max_length=128, blank=False, null=False) 

    # Modification fields
    published       = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Published At')

    # Content fields
    comment         = models.TextField(blank=False, null=False)
    content_type    = models.CharField(choices=CONTENT_TYPE_OPTIONS, max_length=32, verbose_name='Content Type')

    def __str__(self):
        return f'Comment by: {self.author} on : {self.post}, {self.comment}'