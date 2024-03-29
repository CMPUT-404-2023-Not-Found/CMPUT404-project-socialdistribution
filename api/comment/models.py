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
    # auto_now: for saving the time every time the field is saved. Useful for last modified
    # auto_now_add: for saving the time only when the object is created
    published       = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Published At')

    # Content fields
    comment         = models.TextField(blank=False, null=False)
    content_type    = models.CharField(choices=CONTENT_TYPE_OPTIONS, max_length=32, verbose_name='Content Type')

    def __str__(self):
        return f'Comment by: {self.author} on : {self.post}, {self.comment}'

    def get_node_id(self):
        return f'{self.post.get_node_id()}/comments/{self.id}'
